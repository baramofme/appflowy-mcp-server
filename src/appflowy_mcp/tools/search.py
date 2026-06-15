import json

from appflowy_mcp.mcp_instance import mcp
from appflowy_mcp.client import get_client
from appflowy_mcp.config import CHARACTER_LIMIT
from appflowy_mcp.models import SearchInput


@mcp.tool(name="appflowy_search", annotations={"readOnlyHint": True})
async def appflowy_search(params: SearchInput) -> str:
    """Recherche full-text dans AppFlowy Cloud.

    Cherche dans tous les documents, pages et databases.
    Nécessite le service appflowy_search (self-hosted uniquement si configuré).
    """
    client = get_client()
    data = await client.request(
        "GET",
        f"/api/search/{params.workspace_id}",
        params={"query": params.query, "limit": params.limit},
    )
    results = data.get("items", data) if isinstance(data, dict) else data
    if isinstance(results, list):
        results = results[: params.limit]
    return json.dumps(results, indent=2)[:CHARACTER_LIMIT]
