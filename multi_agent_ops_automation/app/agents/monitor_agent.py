from typing import Dict, Any, List
from app.core.config import settings

class MonitorAgent:
    name = "MonitorAgent"

    def check(self, metric: Dict[str, Any]) -> Dict[str, Any]:
        problems: List[str] = []
        level = "INFO"

        if metric["cpu"] >= settings.cpu_alert_threshold:
            problems.append(f"CPU过高：{metric['cpu']}%")
            level = "WARNING"
        if metric["memory"] >= settings.memory_alert_threshold:
            problems.append(f"内存过高：{metric['memory']}%")
            level = "WARNING"
        if metric["disk"] >= settings.disk_alert_threshold:
            problems.append(f"磁盘过高：{metric['disk']}%")
            level = "WARNING"
        if metric.get("error_rate", 0) >= 5:
            problems.append(f"错误率过高：{metric['error_rate']}%")
            level = "CRITICAL"
        if metric.get("latency_ms", 0) >= 1000:
            problems.append(f"接口延迟过高：{metric['latency_ms']}ms")
            level = "WARNING" if level != "CRITICAL" else level

        return {
            "has_incident": len(problems) > 0,
            "level": level,
            "problems": problems,
            "summary": "；".join(problems) if problems else "系统指标正常",
        }
