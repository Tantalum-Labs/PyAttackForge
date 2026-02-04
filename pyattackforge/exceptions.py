"""SDK exception types."""

from typing import Optional


class AttackForgeError(Exception):
    """Base exception for SDK errors."""


class ConfigError(AttackForgeError):
    """Raised when required configuration is missing or invalid."""


class APIError(AttackForgeError):
    """Raised for non-successful HTTP responses."""

    def __init__(self, status_code: int, message: str, payload: Optional[dict] = None) -> None:
        super().__init__(f"HTTP {status_code}: {message}")
        self.status_code = status_code
        self.message = message
        self.payload = payload or {}
