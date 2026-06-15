import httpx
from appflowy_mcp.mcp_instance import mcp
from appflowy_mcp.config import APPFLOWY_BASE_URL
from appflowy_mcp.models import OAuthTokenInput


@mcp.tool(name="appflowy_auth_oauth_token", annotations={"readOnlyHint": True})
async def appflowy_auth_oauth_token(params: OAuthTokenInput) -> str:
    async with httpx.AsyncClient() as hc:
        params_dict = {
            "code": params.code,
            "grant_type": params.grant_type,
            "client_id": params.client_id,
            "client_secret": params.client_secret,
            "redirect_uri": params.redirect_uri,
            "code_verifier": params.code_verifier,
        }
        filtered = {k: v for k, v in params_dict.items() if v is not None}
        url = f"{APPFLOWY_BASE_URL}/web-api/oauth-redirect/token"
        resp = await hc.get(url, params=filtered)
        resp.raise_for_status()
        return resp.text
