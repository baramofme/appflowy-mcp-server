import json

from appflowy_mcp.mcp_instance import mcp
from appflowy_mcp.client import get_client
from appflowy_mcp.models import InviteMemberInput


@mcp.tool(name="appflowy_list_members", annotations={"readOnlyHint": True})
async def appflowy_list_members(workspace_id: str) -> str:
    """Liste les membres d'un workspace avec leurs rôles.

    Retourne email, rôle, et date d'adhésion.
    """
    client = get_client()
    data = await client.request("GET", f"/api/workspace/{workspace_id}/member")
    return json.dumps(data, indent=2)


@mcp.tool(name="appflowy_invite_member", annotations={"readOnlyHint": False, "destructiveHint": False})
async def appflowy_invite_member(params: InviteMemberInput) -> str:
    """Invite un membre dans un workspace AppFlowy.

    Envoie une invitation par email avec le rôle spécifié.
    Le body doit être un tableau (l'API attend Vec<InviteMemberRequest>).
    """
    client = get_client()
    data = await client.request(
        "POST",
        f"/api/workspace/{params.workspace_id}/invite",
        json=[{"email": params.email, "role": params.role.value}],
    )
    return json.dumps(data, indent=2)
