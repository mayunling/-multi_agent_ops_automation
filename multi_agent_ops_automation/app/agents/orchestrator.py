from typing import Dict, Any
from app.agents.monitor_agent import MonitorAgent
from app.agents.analysis_agent import AnalysisAgent
from app.agents.resolver_agent import ResolverAgent
from app.agents.report_agent import ReportAgent
from app.services import db

class OpsOrchestrator:
    """多Agent编排器：监控 -> 分析 -> 处置建议 -> 报告。"""

    def __init__(self) -> None:
        self.monitor = MonitorAgent()
        self.analysis = AnalysisAgent()
        self.resolver = ResolverAgent()
        self.reporter = ReportAgent()

    def run_once(self, metric: Dict[str, Any]) -> Dict[str, Any]:
        metric_id = db.insert_metric(metric)

        monitor_result = self.monitor.check(metric)
        db.log_agent(None, self.monitor.name, monitor_result["summary"], monitor_result)

        if not monitor_result["has_incident"]:
            return {
                "metric_id": metric_id,
                "incident_created": False,
                "message": "指标正常，未创建事件",
                "monitor": monitor_result,
            }

        incident = {
            "service_name": metric["service_name"],
            "level": monitor_result["level"],
            "title": f"{metric['service_name']} 出现{monitor_result['level']}告警",
            "description": monitor_result["summary"],
            "status": "OPEN",
        }
        incident_id = db.create_incident(incident)

        analysis_result = self.analysis.analyze(metric, monitor_result)
        db.update_incident(incident_id, root_cause=analysis_result["root_cause"])
        db.log_agent(incident_id, self.analysis.name, analysis_result["summary"], analysis_result)

        resolver_result = self.resolver.propose(metric)
        db.update_incident(incident_id, actions=resolver_result["actions"])
        db.log_agent(incident_id, self.resolver.name, resolver_result["summary"], resolver_result)

        saved_incident = db.get_incident(incident_id)
        report_result = self.reporter.build_report(saved_incident, resolver_result["actions"])
        db.log_agent(incident_id, self.reporter.name, report_result["summary"], report_result)

        return {
            "metric_id": metric_id,
            "incident_created": True,
            "incident_id": incident_id,
            "monitor": monitor_result,
            "analysis": analysis_result,
            "resolver": resolver_result,
            "report": report_result["report"],
        }
