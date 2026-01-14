"""API key type definitions."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class ApiKey(BaseModel):
    """An API key."""

    id: str
    name: str
    key_prefix: str
    key_suffix: str
    created_at: datetime
    last_used_at: datetime | None = None


class ApiKeyListResponse(BaseModel):
    """Response containing a list of API keys."""

    api_keys: list[ApiKey]


class ApiKeyCreateResponse(BaseModel):
    """Response from creating an API key."""

    id: str
    name: str
    key_value: str
    created_at: datetime

