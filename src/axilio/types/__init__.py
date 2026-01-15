"""Type definitions for Axilio SDK."""

from .api_keys import ApiKey, ApiKeyCreateResponse, ApiKeyListResponse
from .devices import (
    AllocateDeviceResponse,
    AvailableDevicesResponse,
    DeallocateDeviceResponse,
    Device,
    DeviceStatus,
    DeviceType,
)
from .runs import Run, RunConfig, RunStatus, RunTrigger
from .workflows import NodeVariableInfo, WorkflowExecuteResponse, WorkflowVariablesResponse

__all__ = [
    # Devices
    "DeviceType",
    "DeviceStatus",
    "Device",
    "AvailableDevicesResponse",
    "AllocateDeviceResponse",
    "DeallocateDeviceResponse",
    # API Keys
    "ApiKey",
    "ApiKeyListResponse",
    "ApiKeyCreateResponse",
    # Workflows
    "NodeVariableInfo",
    "WorkflowVariablesResponse",
    "WorkflowExecuteResponse",
    # Runs
    "RunStatus",
    "RunTrigger",
    "RunConfig",
    "Run",
]
