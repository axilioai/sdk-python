"""
Axilio Python SDK

A lightweight SDK for the Axilio mobile device automation platform.

Usage:
    >>> from axilio import Client
    >>> client = Client(api_key="ax_live_...")
    >>>
    >>> # List available devices
    >>> devices = client.devices.list_available()
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
    RunStatus,
    RunTrigger,
    WorkflowExecuteResponse,
    WorkflowVariablesResponse,
)  # noqa: F401 - re-exported from types package

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
    "NodeVariableInfo",
    "WorkflowExecuteResponse",
    "WorkflowVariablesResponse",
]
