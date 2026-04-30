from app.services import db
from app.agents.orchestrator import OpsOrchestrator

db.init_db()
orch = OpsOrchestrator()
examples = [
    {"service_name":"campus-api","cpu":92,"memory":72,"disk":55,"error_rate":1.2,"latency_ms":380},
    {"service_name":"ai-assistant","cpu":45,"memory":91,"disk":61,"error_rate":2.1,"latency_ms":820},
    {"service_name":"gateway","cpu":66,"memory":64,"disk":93,"error_rate":0.5,"latency_ms":260},
    {"service_name":"user-center","cpu":70,"memory":60,"disk":50,"error_rate":7.8,"latency_ms":1300},
]
for e in examples:
    print(orch.run_once(e))
