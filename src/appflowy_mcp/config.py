"""Configuration constants for the AppFlowy MCP server."""
import os

APPFLOWY_BASE_URL = os.environ.get("APPFLOWY_BASE_URL", "https://api.appflowy.io")
APPFLOWY_GOTRUE_URL = os.environ.get("APPFLOWY_GOTRUE_URL", f"{APPFLOWY_BASE_URL}/gotrue")
APPFLOWY_WS_URL = os.environ.get("APPFLOWY_WS_URL", f"wss://api.appflowy.io/ws")
CHARACTER_LIMIT = 25000
