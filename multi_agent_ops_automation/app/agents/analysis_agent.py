from typing import Dict, Any

class AnalysisAgent:
    name = "AnalysisAgent"

    def analyze(self, metric: Dict[str, Any], monitor_result: Dict[str, Any]) -> Dict[str, Any]:
        causes = []
        if metric["cpu"] >= 85:
            causes.append("可能存在计算密集任务、死循环、突发流量或进程异常占用CPU")
        if metric["memory"] >= 85:
            causes.append("可能存在内存泄漏、缓存未释放或并发请求过多")
        if metric["disk"] >= 90:
            causes.append("可能存在日志堆积、上传文件过多或临时文件未清理")
        if metric.get("error_rate", 0) >= 5:
            causes.append("可能存在接口异常、数据库连接失败、第三方服务不可用或新版本发布问题")
        if metric.get("latency_ms", 0) >= 1000:
            causes.append("可能存在慢SQL、网络抖动、下游服务超时或线程池耗尽")

        root_cause = "；".join(causes) if causes else "暂无明显异常原因"
        return {
            "root_cause": root_cause,
            "risk": "高" if monitor_result["level"] == "CRITICAL" else "中",
            "summary": f"初步根因分析：{root_cause}",
        }
