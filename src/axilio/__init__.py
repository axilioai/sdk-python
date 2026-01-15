"""
Axilio Python SDK

A lightweight SDK for the Axilio mobile device automation platform.

Usage:
    >>> from axilio import Client, RunConfig
    >>> client = Client(api_key="ax_live_...")
    >>>
    >>> # Execute a workflow
    >>> result = client.workflows.execute(
    ...     workflow_id="abc123",
    ...     runs=[RunConfig(variables=[{"node_id": "value"}])]
    ... )
"""

from .client import Client
from .exceptions import (
    APIError,
    AuthenticationError,
    AxilioError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)
from .types import (
    AllocateDeviceResponse,
    ApiKey,
    ApiKeyCreateResponse,
    ApiKeyListResponse,
    AvailableDevicesResponse,
    DeallocateDeviceResponse,
    Device,
    DeviceStatus,
    DeviceType,
    NodeVariableInfo,
    Run,
    RunConfig,
    RunStatus,
    RunTrigger,
    WorkflowExecuteResponse,
    WorkflowVariablesResponse,
)

__version__ = "0.1.0"

__all__ = [
    # Client
    "Client",
    # Exceptions
    "AxilioError",
    "APIError",
    "AuthenticationError",
    "NotFoundError",
    "ValidationError",
    "RateLimitError",
    # Types - Enums
    "DeviceType",
    "DeviceStatus",
    "RunStatus",
    "RunTrigger",
    # Types - Models
    "Device",
    "AvailableDevicesResponse",
    "AllocateDeviceResponse",
    "DeallocateDeviceResponse",
    "ApiKey",
    "ApiKeyListResponse",
    "ApiKeyCreateResponse",
    "Run",
    "RunConfig",
    "NodeVariableInfo",
    "WorkflowExecuteResponse",
    "WorkflowVariablesResponse",
]
