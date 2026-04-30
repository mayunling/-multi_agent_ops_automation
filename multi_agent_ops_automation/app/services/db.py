import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional
from app.core.config import settings

DB = Path(settings.db_path)

SCHEMA = """
CREATE TABLE IF NOT EXISTS metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_name TEXT NOT NULL,
    cpu REAL NOT NULL,
    memory REAL NOT NULL,
    disk REAL NOT NULL,
    error_rate REAL NOT NULL,
    latency_ms REAL NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_name TEXT NOT NULL,
    level TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'OPEN',
    root_cause TEXT,
    actions TEXT DEFAULT '[]',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS agent_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_id INTEGER,
    agent TEXT NOT NULL,
    summary TEXT NOT NULL,
    data TEXT DEFAULT '{}',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

def conn() -> sqlite3.Connection:
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

def init_db() -> None:
    with conn() as c:
        c.executescript(SCHEMA)

def insert_metric(metric: Dict[str, Any]) -> int:
    with conn() as c:
        cur = c.execute(
            "INSERT INTO metrics(service_name,cpu,memory,disk,error_rate,latency_ms) VALUES(?,?,?,?,?,?)",
            (metric["service_name"], metric["cpu"], metric["memory"], metric["disk"], metric["error_rate"], metric["latency_ms"]),
        )
        return int(cur.lastrowid)

def list_metrics(limit: int = 50) -> List[Dict[str, Any]]:
    with conn() as c:
        rows = c.execute("SELECT * FROM metrics ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [dict(r) for r in rows]

def create_incident(incident: Dict[str, Any]) -> int:
    with conn() as c:
        cur = c.execute(
            "INSERT INTO incidents(service_name,level,title,description,status,root_cause,actions) VALUES(?,?,?,?,?,?,?)",
            (incident["service_name"], incident["level"], incident["title"], incident["description"], incident.get("status", "OPEN"), incident.get("root_cause"), json.dumps(incident.get("actions", []), ensure_ascii=False)),
        )
        return int(cur.lastrowid)

def update_incident(incident_id: int, **fields: Any) -> None:
    if not fields:
        return
    if "actions" in fields and not isinstance(fields["actions"], str):
        fields["actions"] = json.dumps(fields["actions"], ensure_ascii=False)
    keys = ", ".join([f"{k}=?" for k in fields.keys()])
    values = list(fields.values()) + [incident_id]
    with conn() as c:
        c.execute(f"UPDATE incidents SET {keys}, updated_at=CURRENT_TIMESTAMP WHERE id=?", values)

def get_incident(incident_id: int) -> Optional[Dict[str, Any]]:
    with conn() as c:
        row = c.execute("SELECT * FROM incidents WHERE id=?", (incident_id,)).fetchone()
        if not row:
            return None
        item = dict(row)
        item["actions"] = json.loads(item.get("actions") or "[]")
        return item

def list_incidents(limit: int = 50) -> List[Dict[str, Any]]:
    with conn() as c:
        rows = c.execute("SELECT * FROM incidents ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        out = []
        for r in rows:
            item = dict(r)
            item["actions"] = json.loads(item.get("actions") or "[]")
            out.append(item)
        return out

def log_agent(incident_id: int | None, agent: str, summary: str, data: Dict[str, Any] | None = None) -> None:
    with conn() as c:
        c.execute(
            "INSERT INTO agent_logs(incident_id,agent,summary,data) VALUES(?,?,?,?)",
            (incident_id, agent, summary, json.dumps(data or {}, ensure_ascii=False)),
        )

def list_agent_logs(limit: int = 100) -> List[Dict[str, Any]]:
    with conn() as c:
        rows = c.execute("SELECT * FROM agent_logs ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        out = []
        for r in rows:
            item = dict(r)
            item["data"] = json.loads(item.get("data") or "{}")
            out.append(item)
        return out
