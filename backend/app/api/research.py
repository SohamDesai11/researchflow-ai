from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, status

from app.schemas.research import (
    ResearchJob,
    ResearchRequest,
    ResearchStatus,
)

router = APIRouter(prefix="/research", tags=["Research"])

research_jobs: dict[UUID, ResearchJob] = {}


@router.post(
    "",
    response_model=ResearchJob,
    status_code=status.HTTP_201_CREATED,
)
async def create_research(
    request: ResearchRequest,
):
    job = ResearchJob(
        research_id=uuid4(),
        question=request.question,
        depth=request.depth,
        status=ResearchStatus.queued,
        created_at=datetime.now(timezone.utc),
    )

    research_jobs[job.research_id] = job

    return job


@router.get(
    "/{research_id}",
    response_model=ResearchJob,
)
async def get_research(research_id: UUID):
    job = research_jobs.get(research_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Research job not found",
        )

    return job
