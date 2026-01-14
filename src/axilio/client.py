"""Axilio API client."""

from __future__ import annotations

import os
from typing import Any

from ._http import HTTPClient
from .resources import Workflows

DEFAULT_BASE_URL = "https://api.axilio.com"


class Client:
    """
    Axilio API client.

    Usage:
        >>> from axilio import Client
        >>> client = Client(api_key="ax_live_...")
        >>>
        >>> # List available devices
        >>> devices = client.devices.list_available()
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float = 30.0,
    ):
        """
        Initialize the Axilio client.

        Args:
            api_key: Your Axilio API key. If not provided, reads from AXILIO_API_KEY env var.
            base_url: API base URL. Defaults to https://api.axilio.com
            timeout: Request timeout in seconds. Defaults to 30.
        """
        api_key = api_key or os.environ.get("AXILIO_API_KEY")
        if not api_key:
            raise ValueError(
                "API key is required. Pass it as an argument or set AXILIO_API_KEY environment variable."
            )

        base_url = base_url or os.environ.get("AXILIO_BASE_URL", DEFAULT_BASE_URL)

        self._http = HTTPClient(api_key=api_key, base_url=base_url, timeout=timeout)

        # Resources
        self.workflows = Workflows(self._http)

    def close(self) -> None:
        """Close the client and release resources."""
        self._http.close()

    def __enter__(self) -> "Client":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
