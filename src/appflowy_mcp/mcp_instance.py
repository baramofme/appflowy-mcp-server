"""FastMCP instance singleton — created before any tool modules import it."""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("appflowy_mcp")
