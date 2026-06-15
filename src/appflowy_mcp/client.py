"""HTTP client for AppFlowy Cloud API."""
import os
from typing import Optional, Dict, Any

import httpx

from appflowy_mcp.config import APPFLOWY_BASE_URL


class AppFlowyClient:
    """Client HTTP pour AppFlowy Cloud API."""

    def __init__(self, base_url: str = "", token: str = ""):
        self.base_url = (base_url or APPFLOWY_BASE_URL).rstrip("/")
        self.token = token or os.environ.get("APPFLOWY_TOKEN", "")
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )

    async def request(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        resp = await self.client.request(method, path, **kwargs)
        resp.raise_for_status()
        return resp.json()

    async def close(self):
        await self.client.aclose()


_client: Optional[AppFlowyClient] = None


def get_client() -> AppFlowyClient:
    global _client
    if _client is None:
        _client = AppFlowyClient()
    return _client


def set_client(client: AppFlowyClient) -> None:
    """Replace the global client (used by auth_login to inject a new token)."""
    global _client
    _client = client
