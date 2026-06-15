import json

from appflowy_mcp.mcp_instance import mcp
from appflowy_mcp.client import get_client
from appflowy_mcp.config import CHARACTER_LIMIT
from appflowy_mcp.models import CreateWorkspaceInput


@mcp.tool(name="appflowy_list_workspaces", annotations={"readOnlyHint": True})
async def appflowy_list_workspaces() -> str:
    client = get_client()
    raw = await client.request("GET", "/api/workspace")
    inner = raw.get("data", raw)
    workspaces = inner if isinstance(inner, list) else inner.get("data", [])
    result = []
    for ws in workspaces[:20]:
        result.append({
            "workspace_id": ws.get("workspace_id", ""),
            "name": ws.get("workspace_name", ""),
            "role": ws.get("role", ""),
        })
    return json.dumps(result, indent=2)


@mcp.tool(name="appflowy_create_workspace", annotations={"readOnlyHint": False, "destructiveHint": False})
async def appflowy_create_workspace(params: CreateWorkspaceInput) -> str:
    client = get_client()
    data = await client.request("POST", "/api/workspace", json={"workspace_name": params.name})
    return json.dumps(data, indent=2)


@mcp.tool(name="appflowy_get_folder", annotations={"readOnlyHint": True})
async def appflowy_get_folder(workspace_id: str) -> str:
    client = get_client()
    data = await client.request("GET", f"/api/workspace/{workspace_id}/folder")
    result = json.dumps(data, indent=2)
    return result[:CHARACTER_LIMIT] if len(result) > CHARACTER_LIMIT else result
