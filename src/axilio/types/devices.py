"""Device type definitions."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class DeviceType(str, Enum):
    """Type of device."""

    IPHONE = "IPHONE"
    ANDROID = "ANDROID"
    UNKNOWN = "UNKNOWN"


class DeviceStatus(str, Enum):
    """Status of a device."""

    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    MAINTENANCE = "MAINTENANCE"
    SUSPENDED = "SUSPENDED"


class Device(BaseModel):
    """A device in the Axilio platform."""

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
    """Response containing available devices."""

    iphone_count: int
    android_count: int
    devices: list[Device]


class AllocateDeviceResponse(BaseModel):
    """Response from allocating a device."""

    device_id: str
    workflow_started_at: datetime
    region: str | None = None


class DeallocateDeviceResponse(BaseModel):
    """Response from deallocating a device."""

    device_id: str
    workflow_id: str
    billing_session_id: str

