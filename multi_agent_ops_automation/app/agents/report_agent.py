from typing import Dict, Any, List

class ReportAgent:
    name = "ReportAgent"

    def build_report(self, incident: Dict[str, Any], actions: List[str]) -> Dict[str, Any]:
        report = f"""
【运维事件报告】
服务名称：{incident['service_name']}
告警级别：{incident['level']}
事件标题：{incident['title']}
当前状态：{incident['status']}

【问题描述】
{incident['description']}

【初步根因】
{incident.get('root_cause') or '待分析'}

【建议处理步骤】
{chr(10).join([f'{i+1}. {a}' for i, a in enumerate(actions)])}
""".strip()
        return {"report": report, "summary": "已生成事件报告"}
