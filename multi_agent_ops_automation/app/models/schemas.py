from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from datetime import datetime

class MetricInput(BaseModel):
    service_name: str = Field(..., examples=["campus-api"])
    cpu: float = Field(..., ge=0, le=100)
    memory: float = Field(..., ge=0, le=100)
    disk: float = Field(..., ge=0, le=100)
    error_rate: float = Field(0, ge=0, le=100)
    latency_ms: float = Field(0, ge=0)

class Incident(BaseModel):
    id: Optional[int] = None
    service_name: str
    level: str
    title: str
    description: str
    status: str = "OPEN"
    root_cause: Optional[str] = None
    actions: List[str] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class AgentResult(BaseModel):
    agent: str
    summary: str
    data: Dict[str, Any] = {}
