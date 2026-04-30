from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.models.schemas import MetricInput
from app.services import db
from app.services.scheduler import start_scheduler, stop_scheduler, orchestrator

app = FastAPI(title="Multi-Agent Ops Automation")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
def on_startup() -> None:
    db.init_db()

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "incidents": db.list_incidents(20),
        "metrics": db.list_metrics(20),
        "logs": db.list_agent_logs(30),
    })

@app.post("/api/metrics")
def submit_metric(metric: MetricInput):
    return orchestrator.run_once(metric.model_dump())

@app.get("/api/incidents")
def incidents(limit: int = 50):
    return db.list_incidents(limit)

@app.get("/api/metrics")
def metrics(limit: int = 50):
    return db.list_metrics(limit)

@app.get("/api/logs")
def logs(limit: int = 100):
    return db.list_agent_logs(limit)

@app.post("/api/incidents/{incident_id}/close")
def close_incident(incident_id: int):
    item = db.get_incident(incident_id)
    if not item:
        raise HTTPException(status_code=404, detail="事件不存在")
    db.update_incident(incident_id, status="CLOSED")
    return {"ok": True, "message": "事件已关闭"}

@app.get("/api/incidents/{incident_id}/report", response_class=PlainTextResponse)
def report(incident_id: int):
    item = db.get_incident(incident_id)
    if not item:
        raise HTTPException(status_code=404, detail="事件不存在")
    actions = item.get("actions", [])
    return f"""
【运维事件报告】
服务名称：{item['service_name']}
告警级别：{item['level']}
事件标题：{item['title']}
当前状态：{item['status']}
创建时间：{item['created_at']}
更新时间：{item['updated_at']}

【问题描述】
{item['description']}

【初步根因】
{item.get('root_cause') or '待分析'}

【建议处理步骤】
{chr(10).join([f'{i+1}. {a}' for i, a in enumerate(actions)])}
""".strip()

@app.post("/api/scheduler/start")
def api_start_scheduler():
    start_scheduler()
    return {"ok": True, "message": "模拟监控任务已启动，每15秒生成一次指标"}

@app.post("/api/scheduler/stop")
def api_stop_scheduler():
    stop_scheduler()
    return {"ok": True, "message": "模拟监控任务已停止"}
