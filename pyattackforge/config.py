"""Configuration helpers."""

from dataclasses import dataclass
import os
from typing import Optional

from .exceptions import ConfigError


@dataclass(frozen=True)
class ClientConfig:
    base_url: str
    api_key: str
    ui_base_url: Optional[str] = None
    ui_token: Optional[str] = None
    timeout: float = 30.0
    max_retries: int = 3
    backoff_factor: float = 0.5
    user_agent: str = "pyattackforge/0.2.3"
    http2: bool = True
    # Default visibility for newly created findings. False = pending/hidden.
    default_findings_visible: bool = False
    # Default substatus custom field for newly created findings.
    default_findings_substatus_key: Optional[str] = "substatus"
    default_findings_substatus_value: Optional[str] = "Observed"


def config_from_env() -> ClientConfig:
    base_url = os.getenv("ATTACKFORGE_BASE_URL")
    api_key = os.getenv("ATTACKFORGE_API_KEY")
    if not base_url or not api_key:
        raise ConfigError("ATTACKFORGE_BASE_URL and ATTACKFORGE_API_KEY are required")
    ui_base_url = os.getenv("ATTACKFORGE_UI_BASE_URL")
    ui_token = os.getenv("ATTACKFORGE_UI_TOKEN")
    visible_env = os.getenv("ATTACKFORGE_FINDINGS_VISIBLE_DEFAULT")
    substatus_key_env = os.getenv("ATTACKFORGE_FINDINGS_SUBSTATUS_KEY")
    substatus_value_env = os.getenv("ATTACKFORGE_FINDINGS_SUBSTATUS_VALUE")
    default_visible = False
    if visible_env is not None:
        default_visible = visible_env.strip().lower() in {"1", "true", "yes", "y", "visible"}
    return ClientConfig(
        base_url=base_url,
        api_key=api_key,
        ui_base_url=ui_base_url,
        ui_token=ui_token,
        default_findings_visible=default_visible,
        default_findings_substatus_key=_normalize_default_substatus(substatus_key_env, "substatus"),
        default_findings_substatus_value=_normalize_default_substatus(substatus_value_env, "Observed"),
    )


def _normalize_default_substatus(value: Optional[str], default: str) -> Optional[str]:
    if value is None:
        return default
    cleaned = value.strip()
    if not cleaned:
        return None
    lowered = cleaned.lower()
    if lowered in {"none", "null", "false", "0", "off", "disable", "disabled"}:
        return None
    return cleaned
