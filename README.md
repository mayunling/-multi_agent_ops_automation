[README.md](https://github.com/user-attachments/files/27240372/README.md)
# 多Agent系统运营自动化系统

这是一个可直接运行的多 Agent 运维自动化 MVP，适合课程设计、项目展示、比赛原型和简历项目扩展。

## 功能

- 指标采集：CPU、内存、磁盘、错误率、接口延迟
- MonitorAgent：判断是否触发告警
- AnalysisAgent：分析可能根因
- ResolverAgent：生成处理建议
- ReportAgent：生成事件报告
- Orchestrator：统一编排多个 Agent
- FastAPI 接口
- Web 控制台
- SQLite 数据持久化
- 定时模拟监控任务

## 运行

```bash
cd multi_agent_ops_automation
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

浏览器打开：

```text
http://127.0.0.1:8000
```

## 初始化测试数据

```bash
python scripts/seed.py
```

## 手动调用接口

```bash
curl -X POST http://127.0.0.1:8000/api/metrics \
  -H "Content-Type: application/json" \
  -d '{"service_name":"campus-api","cpu":91,"memory":70,"disk":60,"error_rate":1,"latency_ms":300}'
```

## 项目结构

```text
app/
  agents/              # 多Agent核心
  core/                # 配置
  models/              # Pydantic模型
  services/            # 数据库、调度器
  static/              # 前端JS/CSS
  templates/           # 页面模板
scripts/seed.py        # 测试数据
```

## 后续可扩展方向

1. 接入 Prometheus / Grafana / Loki。
2. 接入企业微信、飞书、邮件通知。
3. ResolverAgent 增加自动执行脚本能力。
4. AnalysisAgent 接入大模型做日志总结和根因分析。
5. 增加用户登录、权限管理、工单流转。
