import random
from apscheduler.schedulers.background import BackgroundScheduler
from app.agents.orchestrator import OpsOrchestrator

scheduler = BackgroundScheduler()
orchestrator = OpsOrchestrator()

def mock_collect_metric() -> None:
    """模拟采集指标。真实项目可替换为 Prometheus、服务器脚本、日志平台接口。"""
    metric = {
        "service_name": random.choice(["campus-api", "user-center", "ai-assistant", "gateway"]),
        "cpu": round(random.uniform(20, 96), 2),
        "memory": round(random.uniform(30, 96), 2),
        "disk": round(random.uniform(40, 95), 2),
        "error_rate": round(random.uniform(0, 8), 2),
        "latency_ms": round(random.uniform(80, 1500), 2),
    }
    orchestrator.run_once(metric)

def start_scheduler() -> None:
    if not scheduler.running:
        scheduler.add_job(mock_collect_metric, "interval", seconds=15, id="mock_metric_job", replace_existing=True)
        scheduler.start()

def stop_scheduler() -> None:
    if scheduler.running:
        scheduler.shutdown(wait=False)
