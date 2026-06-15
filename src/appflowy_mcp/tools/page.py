"""Page-related MCP tools."""
import json
from appflowy_mcp.mcp_instance import mcp
from appflowy_mcp.client import get_client
from appflowy_mcp.config import CHARACTER_LIMIT
from appflowy_mcp.models import CreatePageInput, GetPageInput, AppendBlockInput, UpdatePageNameInput, AFViewType


@mcp.tool(name="appflowy_create_page", annotations={"readOnlyHint": False, "destructiveHint": False})
async def appflowy_create_page(params: CreatePageInput) -> str:
    client = get_client()
    view_layout_map = {"document": 0, "grid": 1, "board": 2, "calendar": 3, "space": 0}
    layout = params.layout if params.layout != 0 else view_layout_map.get(params.view_type.value, 0)

    body = {
        "parent_view_id": params.parent_view_id,
        "layout": layout,
        "name": params.name,
    }
    if params.page_data is not None:
        body["page_data"] = params.page_data
    data = await client.request("POST", f"/api/workspace/{params.workspace_id}/page-view", json=body)
    return json.dumps(data, indent=2)


@mcp.tool(name="appflowy_get_page", annotations={"readOnlyHint": True})
async def appflowy_get_page(params: GetPageInput) -> str:
    client = get_client()
    data = await client.request(
        "GET",
        f"/api/workspace/{params.workspace_id}/page-view/{params.view_id}",
    )
    result = json.dumps(data, indent=2)
    return result[:CHARACTER_LIMIT] if len(result) > CHARACTER_LIMIT else result


@mcp.tool(name="appflowy_append_block", annotations={"readOnlyHint": False, "destructiveHint": False})
async def appflowy_append_block(params: AppendBlockInput) -> str:
    client = get_client()
    data = await client.request(
        "POST",
        f"/api/workspace/{params.workspace_id}/page-view/{params.view_id}/append-block",
        json={"blocks": params.blocks},
    )
    return json.dumps(data, indent=2)


@mcp.tool(name="appflowy_update_page_name", annotations={"readOnlyHint": False, "destructiveHint": False})
async def appflowy_update_page_name(params: UpdatePageNameInput) -> str:
    client = get_client()
    data = await client.request(
        "POST",
        f"/api/workspace/{params.workspace_id}/page-view/{params.view_id}/update-name",
        json={"name": params.name},
    )
    return json.dumps(data, indent=2)
