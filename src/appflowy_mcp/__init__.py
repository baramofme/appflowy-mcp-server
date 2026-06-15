"""AppFlowy MCP server package.

Usage:
    from appflowy_mcp import mcp
    mcp.run()
"""
from appflowy_mcp.mcp_instance import mcp

# Import all tool modules to register them with the MCP server
from appflowy_mcp.tools import (
    auth,
    workspace,
    page,
    search,
    collab,
    member,
    health,
    database,
    oauth,
)

__all__ = ["mcp"]
