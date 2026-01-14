"""Axilio SDK exceptions."""

from __future__ import annotations


class AxilioError(Exception):
    """Base exception for Axilio SDK."""

    pass


class AuthenticationError(AxilioError):
    """Raised when authentication fails."""

    pass


class APIError(AxilioError):
    """Raised when the API returns an error response."""

    def __init__(self, message: str, status_code: int, response_body: dict | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class NotFoundError(APIError):
    """Raised when a resource is not found (404)."""

    pass


class ValidationError(APIError):
    """Raised when request validation fails (422)."""

    pass


class RateLimitError(APIError):
    """Raised when rate limit is exceeded (429)."""

    pass

