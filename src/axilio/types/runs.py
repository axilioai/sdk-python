"""Run type definitions."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

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
    API = "api"


class RunConfig(BaseModel):
    """Configuration for a single run.
    
    Each RunConfig represents one run's variable configuration.
    Variables is a list with one dict keyed by nodeId, where values
    are the raw values (string, number, boolean, array, object).
    
    Example:
        >>> config = RunConfig(variables=[{"node_abc": "my_value"}])
    """

    variables: list[dict[str, Any]]


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
