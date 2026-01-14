"""HTTP transport layer for Axilio SDK."""

from __future__ import annotations

from typing import Any

import httpx

from .exceptions import (
    APIError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)


class HTTPClient:
    """HTTP client for API requests."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.axilio.com",
        timeout: float = 30.0,
    ):
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            timeout=timeout,
        )

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make an HTTP request and return parsed JSON response."""
        response = self._client.request(method, path, params=params, json=json)
        return self._handle_response(response)

    def get(self, path: str, *, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.request("GET", path, params=params)

    def post(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self.request("POST", path, params=params, json=json)

    def put(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self.request("PUT", path, params=params, json=json)

    def patch(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self.request("PATCH", path, params=params, json=json)

    def delete(self, path: str, *, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.request("DELETE", path, params=params)

    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        """Handle response and raise appropriate exceptions."""
        if response.status_code == 401:
            raise AuthenticationError("Invalid or expired API key")

        try:
            body = response.json() if response.content else {}
        except Exception:
            body = {}

        if response.status_code == 404:
            raise NotFoundError(
                f"Resource not found: {response.url.path}",
                status_code=404,
                response_body=body,
            )

        if response.status_code == 422:
            detail = body.get("detail", "Validation error")
            raise ValidationError(str(detail), status_code=422, response_body=body)

        if response.status_code == 429:
            raise RateLimitError("Rate limit exceeded", status_code=429, response_body=body)

        if response.status_code >= 400:
            message = body.get("detail", body.get("message", f"API error: {response.status_code}"))
            raise APIError(str(message), status_code=response.status_code, response_body=body)

        return body

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self) -> "HTTPClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
