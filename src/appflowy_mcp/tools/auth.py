import json
import os
import httpx
from appflowy_mcp.mcp_instance import mcp
from appflowy_mcp.client import set_client, AppFlowyClient
from appflowy_mcp.config import APPFLOWY_GOTRUE_URL
from appflowy_mcp.models import AuthLoginInput


@mcp.tool(name="appflowy_auth_login", annotations={"readOnlyHint": False, "destructiveHint": False})
async def appflowy_auth_login(params: AuthLoginInput) -> str:
    async with httpx.AsyncClient() as hc:
        resp = await hc.post(
            f"{APPFLOWY_GOTRUE_URL}/token?grant_type=password",
            json={"email": params.email, "password": params.password},
        )
        resp.raise_for_status()
        data = resp.json()
        token = data.get("access_token", "")
        os.environ["APPFLOWY_TOKEN"] = token
        set_client(AppFlowyClient(token=token))
        return json.dumps({"access_token": token[:20] + "...", "expires_in": data.get("expires_in")})
