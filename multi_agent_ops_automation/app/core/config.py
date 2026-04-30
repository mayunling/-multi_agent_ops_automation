from pydantic import BaseModel

class Settings(BaseModel):
    app_name: str = "Multi-Agent Ops Automation"
    db_path: str = "ops.db"
    monitor_interval_seconds: int = 15
    cpu_alert_threshold: float = 85.0
    memory_alert_threshold: float = 85.0
    disk_alert_threshold: float = 90.0

settings = Settings()
