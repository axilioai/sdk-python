"""Type definitions for Axilio SDK."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel


# ============================================================================
# Enums
# ============================================================================


class DeviceType(str, Enum):
    IPHONE = "IPHONE"
    ANDROID = "ANDROID"
    UNKNOWN = "UNKNOWN"


class DeviceStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    MAINTENANCE = "MAINTAINENCE"
    SUSPENDED = "SUSPENDED"


# ============================================================================
# Device Types
# ============================================================================


class Device(BaseModel):
    id: int
    device_id: str
    device_name: str | None = None
    device_type: DeviceType | None = None
    status: DeviceStatus = DeviceStatus.ACTIVE
    model_name: str | None = None
    location: str | None = None
    current_workflow_id: str | None = None
    workflow_started_at: datetime | None = None


class AvailableDevicesResponse(BaseModel):
    iphone_count: int
    android_count: int
    devices: list[Device]


class AllocateDeviceResponse(BaseModel):
    device_id: str
    workflow_started_at: datetime
    region: str | None = None


class DeallocateDeviceResponse(BaseModel):
    device_id: str
    workflow_id: str
    billing_session_id: str


# ============================================================================
# API Key Types
# ============================================================================


class ApiKey(BaseModel):
    id: str
    name: str
    key_prefix: str
    key_suffix: str
    created_at: datetime
    last_used_at: datetime | None = None


class ApiKeyListResponse(BaseModel):
    api_keys: list[ApiKey]


class ApiKeyCreateResponse(BaseModel):
    id: str
    name: str
    key_value: str
    created_at: datetime


class NodeVariableInfo(BaseModel):
    """Information about a node that requires variable input at runtime."""

    node_id: str
    label: str
    order: int
    variable_name: str | None = None


class WorkflowVariablesResponse(BaseModel):
    """Response containing all nodes that require variable input."""

    workflow_id: str
    variables: dict[str, NodeVariableInfo]


class WorkflowExecuteResponse(BaseModel):
    """Response from executing a workflow."""

    run_ids: list[str]
