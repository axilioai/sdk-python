"""Run type definitions."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class RunStatus(str, Enum):
    """Status of a workflow run."""

    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class RunTrigger(str, Enum):
    """How a run was triggered."""

    MANUAL = "manual"
    SCHEDULED = "scheduled"


class Run(BaseModel):
    """A workflow run."""

    id: str
    workflow_id: str
    user_id: str
    device_id: str | None = None
    status: RunStatus
    trigger: RunTrigger
    started_at: datetime | None = None
    completed_at: datetime | None = None
    cancelled_at: datetime | None = None
    success: bool | None = None
    error_message: str | None = None
    logs: str | None = None
    video_url: str | None = None
    create_date: datetime
    update_date: datetime

