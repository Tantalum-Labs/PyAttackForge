"""HTTP transport for AttackForge SSAPI."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional
import time
import httpx

from .exceptions import APIError
from .config import ClientConfig


@dataclass
class TransportResponse:
    status_code: int
    data: Any
    headers: Dict[str, str]


class AttackForgeTransport:
    def __init__(self, config: ClientConfig, client: Optional[httpx.Client] = None) -> None:
        self._config = config
        self._client = client or httpx.Client(
            base_url=config.base_url.rstrip("/"),
            timeout=config.timeout,
            headers={
                "X-SSAPI-KEY": config.api_key,
                "Connection": "close",
                "User-Agent": config.user_agent,
            },
            http2=config.http2,
        )
        self._http2_client: Optional[httpx.Client] = None

    def close(self) -> None:
        self._client.close()
        if self._http2_client is not None:
            self._http2_client.close()

    def _get_http2_client(self) -> httpx.Client:
        if self._http2_client is None:
            self._http2_client = httpx.Client(
                base_url=self._config.base_url.rstrip("/"),
                timeout=self._config.timeout,
                headers={
                    "X-SSAPI-KEY": self._config.api_key,
                    "Connection": "close",
                    "User-Agent": self._config.user_agent,
                },
                http2=True,
            )
        return self._http2_client

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
        retries: Optional[int] = None,
    ) -> TransportResponse:
        attempt = 0
        max_retries = self._config.max_retries if retries is None else retries
        backoff = self._config.backoff_factor
        while True:
            try:
                request_headers = None
                if headers:
                    request_headers = headers
                if files:
                    request_headers = dict(self._client.headers)
                    request_headers.pop("Content-Type", None)
                    if headers:
                        request_headers.update(headers)
                response = self._client.request(
                    method=method,
                    url=path,
                    params=params,
                    json=json,
                    files=files,
                    data=data,
                    headers=request_headers,
                    timeout=timeout,
                )
            except httpx.HTTPError as exc:
                if attempt >= max_retries:
                    raise APIError(status_code=0, message=str(exc)) from exc
                time.sleep(backoff * (2 ** attempt))
                attempt += 1
                continue

            if response.status_code >= 500 and files:
                try:
                    response = self._get_http2_client().request(
                        method=method,
                        url=path,
                        params=params,
                        json=json,
                        files=files,
                        data=data,
                        headers=request_headers,
                        timeout=timeout,
                    )
                except httpx.HTTPError:
                    pass

            if response.status_code in (429, 500, 502, 503, 504) and attempt < max_retries:
                time.sleep(backoff * (2 ** attempt))
                attempt += 1
                continue

            data_out: Any
            if response.headers.get("content-type", "").startswith("application/json"):
                try:
                    data_out = response.json()
                except ValueError:
                    data_out = response.text
            else:
                data_out = response.content

            if response.status_code >= 400:
                raise APIError(response.status_code, response.text, payload={"data": data_out})

            return TransportResponse(
                status_code=response.status_code,
                data=data_out,
                headers=dict(response.headers),
            )
