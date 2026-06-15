import json
import httpx

from appflowy_mcp.mcp_instance import mcp
from appflowy_mcp.config import APPFLOWY_BASE_URL


@mcp.tool(name="appflowy_health_check", annotations={"readOnlyHint": True})
async def appflowy_health_check() -> str:
    """Vérifie la connectivité avec AppFlowy Cloud.

    Utile pour diagnostiquer les problèmes de connexion.
    """
    try:
        async with httpx.AsyncClient() as hc:
            resp = await hc.get(f"{APPFLOWY_BASE_URL}/health", timeout=5.0)
            return json.dumps({"status": "ok" if resp.status_code == 200 else "error", "code": resp.status_code})
    except Exception as e:
        return json.dumps({"status": "unreachable", "error": str(e)})
