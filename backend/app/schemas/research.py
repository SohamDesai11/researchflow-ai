from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class ResearchDepth(str, Enum):
    quick = "quick"
    standard = "standard"
    deep = "deep"


class ResearchStatus(str, Enum):
    queued = "queued"
    running = "running"
    completed = "completed"
    failed = "failed"


class ResearchRequest(BaseModel):
    question: str = Field(
        min_length=10,
        max_length=2000
    )
    depth: ResearchDepth = ResearchDepth.standard


class ResearchJob(BaseModel):
    research_id: UUID
    question: str
    depth: ResearchDepth
    status: ResearchStatus
    created_at: datetime
    report: str | None = None
    error: str | None = None
