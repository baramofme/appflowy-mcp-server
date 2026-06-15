import json

from appflowy_mcp.mcp_instance import mcp
from appflowy_mcp.client import get_client
from appflowy_mcp.config import CHARACTER_LIMIT
from appflowy_mcp.models import CollabGetInput


@mcp.tool(name="appflowy_get_collab", annotations={"readOnlyHint": True})
async def appflowy_get_collab(params: CollabGetInput) -> str:
    """Récupère un objet collaboratif (document, folder, database).

    Utilise l'endpoint V1 : GET /api/workspace/v1/{ws}/collab/{id}?collab_type=N.

    Avec json_format=True : GET .../collab/{id}/json → décode le Yjs en JSON.
    """
    client = get_client()
    path = f"/api/workspace/v1/{params.workspace_id}/collab/{params.object_id}"
    if params.json_format:
        path += "/json"
    data = await client.request(
        "GET",
        path,
        params={"collab_type": params.collab_type},
    )
    return json.dumps(data, indent=2)[:CHARACTER_LIMIT]
