from typing import Dict, Any, List

class ResolverAgent:
    name = "ResolverAgent"

    def propose(self, metric: Dict[str, Any]) -> Dict[str, Any]:
        actions: List[str] = []
        if metric["cpu"] >= 85:
            actions += ["查看CPU占用最高的进程", "临时扩容服务实例", "检查最近是否有高并发请求或异常循环"]
        if metric["memory"] >= 85:
            actions += ["查看内存占用最高的进程", "重启可安全重启的异常服务", "检查缓存、队列和大对象是否释放"]
        if metric["disk"] >= 90:
            actions += ["清理过期日志和临时文件", "检查日志轮转策略", "扩容磁盘或迁移大文件"]
        if metric.get("error_rate", 0) >= 5:
            actions += ["查看最近10分钟错误日志", "检查数据库/Redis/第三方接口状态", "必要时回滚最近发布版本"]
        if metric.get("latency_ms", 0) >= 1000:
            actions += ["排查慢SQL", "检查下游接口耗时", "增加超时保护与降级策略"]

        # 去重但保持顺序
        actions = list(dict.fromkeys(actions))
        return {
            "actions": actions,
            "summary": "建议执行：" + "；".join(actions) if actions else "无需处理",
        }
