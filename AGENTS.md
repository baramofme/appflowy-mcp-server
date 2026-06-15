# AppFlowy MCP Server — Agent Instructions

## Identity

MCP server providing 22 tools to interact with AppFlowy Cloud (self-hosted or SaaS).
Used as a Notion replacement. Docs in French.

## Quick Start

```bash
pip install -r requirements.txt
export APPFLOWY_BASE_URL="https://api.appflowy.io"
export APPFLOWY_TOKEN="<jwt_token>"
python src/appflowy_mcp.py
```

## Source Map

| File | Purpose |
|---|---|
| `src/appflowy_mcp.py` | **Thin entry point** — delegates to `appflowy_mcp` package |
| `src/appflowy_mcp/` | **MCP server package** — `__init__.py`, `config.py`, `client.py`, `models.py`, `mcp_instance.py` |
| `src/appflowy_mcp/tools/` | **Tool modules** — `auth.py`, `workspace.py`, `page.py`, `search.py`, `collab.py`, `member.py`, `health.py`, `database.py`, `oauth.py` |
| `src/jwt_refresh.py` | JWT auto-refresh middleware on 401 (standalone, not wired into appflowy_mcp.py) |
| `src/migrate_notion_to_appflowy.py` | One-shot migration script: Notion API → AppFlowy API |
| `deploy/deploy_appflowy_lxc.py` | LXC container deployment via KIVA orchestrator |
| `deploy/deploy_appflowy_kiva.sh` | Bash variant of LXC deployment for HP Z600 |

## Architecture Notes

- **Package structure**: `appflowy_mcp.py` is a thin entry point (mcp.json compatibility). The `appflowy_mcp/` package contains `config.py`, `client.py`, `models.py`, `mcp_instance.py`, and `tools/` modules.
- **HTTP client**: An `httpx.AsyncClient` singleton (`AppFlowyClient`) with Bearer token auth. Globally cached per process.
- **Token lifecycle**: Set via `APPFLOWY_TOKEN` env var or at runtime via `appflowy_auth_login` tool (GoTrue `grant_type=password`).
  - `token.json` is a cached token artifact (ignored by git if `.gitignore` existed — none exists currently).
- **JWT refresh module** (`jwt_refresh.py`) exists but is **not integrated** into the MCP server. It's a standalone utility — if the server gets a 401, it does NOT auto-refresh currently.
- **CHARACTER_LIMIT = 25000**: All read-only tools truncate responses at this limit.
- **No tests, no linter, no type checker, no formatter** configured in this repo.

## Running

```bash
# MCP server (stdio mode — for MCP-compatible clients like Claude Desktop)
python src/appflowy_mcp.py

# Migration script (requires both tokens)
python src/migrate_notion_to_appflowy.py <appflowy_workspace_id>
```

## Environment Variables

| Variable | Default | Required | Description |
|---|---|---|---|
| `APPFLOWY_BASE_URL` | `https://api.appflowy.io` | No | AppFlowy Cloud API base URL |
| `APPFLOWY_GOTRUE_URL` | `{BASE_URL}/gotrue` | No | GoTrue auth endpoint |
| `APPFLOWY_WS_URL` | `wss://api.appflowy.io/ws` | No | WebSocket URL |
| `APPFLOWY_TOKEN` | — | Yes* | JWT access token (*required for non-auth tools) |
| `APPFLOWY_EMAIL` | — | No | Email for JWT auto-refresh middleware |
| `APPFLOWY_PASSWORD` | — | No | Password for JWT auto-refresh middleware |
| `NOTION_TOKEN` | — | Yes* | Notion API token (*required for migration script) |

## API Endpoint Patterns

All non-auth requests go to `{APPFLOWY_BASE_URL}/api/workspace/{workspace_id}/...`:
- `GET /api/workspace` — list workspaces
- `POST /api/workspace` — create workspace
- `POST /api/workspace/{ws}/page-view` — create page (body: `{parent_view_id, layout, name}`)
  - `parent_view_id` **required** (Uuid — get from folder hierarchy via `get_folder`)
  - `layout` **required** (int: 0=Document, 1=Grid, 2=Board, 3=Calendar)
  - `name` optional (string)
- `GET /api/workspace/{ws}/page-view/{id}` — get page
- `GET /api/workspace/{ws}/folder` — folder hierarchy
- `GET /api/workspace/v1/{ws}/collab/{id}?collab_type=N` — collaborative object (V1 endpoint)
  - `collab_type`: 0=Document, 1=Folder, 2=Database, 3=WorkspaceDatabase, 4=DatabaseRow
  - Note: The non-V1 `GET /api/workspace/{ws}/collab/{id}` is deprecated and returns 400
- `GET /api/workspace/{ws}/member` — list members
- `POST /api/workspace/{ws}/invite` — invite member (body: `[{email, role}]` **array**, not object)
  - `role`: string "Owner"/"Member"/"Guest" (or integer 1/2/3)
- `GET /api/search/{workspace_id}?query=...&limit=...` — full-text search (GET, not POST)
  - `workspace_id` in URL path (required). Query params: `query`, `limit`, `preview_size`, `score`
  - Requires `appflowy_search` microservice (port 4002) to be running
- `GET /api/workspace/{ws}/database` — list databases
- `GET /api/workspace/{ws}/database/{db}/fields` — get database fields
- `POST /api/workspace/{ws}/database/{db}/fields` — create database field (body: `{name, field_type, type_option_data?}`)
- `GET /api/workspace/{ws}/database/{db}/row` — list database row IDs
- `POST /api/workspace/{ws}/database/{db}/row` — create row (body: `{cells, document?}`)
- `PUT /api/workspace/{ws}/database/{db}/row` — upsert row (body: `{pre_hash, cells, document?}`)
- `GET /api/workspace/{ws}/database/{db}/row/detail?ids=...&with_doc=...` — row details
- `GET /api/workspace/{ws}/database/{db}/row/updated?after=...` — recently updated rows
- `GET /web-api/oauth-redirect/token?code=...&grant_type=...&...` — OAuth token exchange
- `GET /health` — health check

View types → ViewLayout mapping: `document→0`, `grid→1`, `board→2`, `calendar→3`, `space→0`.

## BRGS (Branch Routing & Governance System)

The pre-push hook enforces 4 guards against a governance manifest at `GOVERNANCE_HUB_PATH/multi-repo-governance.yaml`:

1. **Remote URL validation** — checks push target matches `gerivdb/{repo_name}`
2. **Ancestry check** — verifies branch is not too far behind/ahead of `main`
3. **Forbidden paths** — blocks files that belong in other repos (redirects to correct repo)
4. **Branch prefix** — validates branch name matches allowed prefixes

A GitHub Action (`.github/workflows/branch-gate.yml`) runs the same checks post-push as a non-blocking warning layer.

The governance manifest and hooks are shared across multiple repos under the ECOS umbrella. The `.githooks/` directory contains both bash (Linux) and PowerShell (cross-platform) hook variants plus a rules generator.

## mcpo (MCP → OpenAPI Proxy)

[mcpo](https://github.com/open-webui/mcpo) wraps stdio MCP servers as REST endpoints.

```bash
pip install mcpo
mcpo --port 8000 --config mcp.json
```

**중요: `mcp.json`의 `env.APPFLOWY_TOKEN`에 `${APPFLOWY_TOKEN}` 같은 환경변수 참조를 쓰면 안 됩니다.** mcpo는 `${VAR}`를 치환하지 않고 그대로 전달합니다. 실제 토큰 값을 직접 넣거나, 실행 전에 `export APPFLOWY_TOKEN=...` 후에 mcp.json을 생성하세요.

**mcpo를 통한 curl 호출 규칙:**
- Pydantic model을 params로 받는 tool → body를 `{"params": {...}}` 로 감싸야 함
  - 대상: `create_workspace`, `create_page`, `get_page`, `search`, `get_collab`, `invite_member`, `auth_login`, `list_databases`, `get_database_fields`, `create_database_field`, `list_database_rows`, `create_database_row`, `upsert_database_row`, `get_database_row_details`, `get_database_row_ids_updated`, `auth_oauth_token`
- 문자열을 직접 params로 받는 tool → body를 `{...}` flat하게 전달
  - 대상: `get_folder(workspace_id)`, `list_members(workspace_id)` (참고: database tool들은 전부 Pydantic model params 사용)
- params 없는 tool → `{}` 빈 body
  - 대상: `list_workspaces`, `health_check`

예시:
```bash
# Pydantic model tool
curl -X POST http://localhost:8000/appflowy/appflowy_get_page \
  -H "Content-Type: application/json" \
  -d '{"params":{"workspace_id":"...","view_id":"..."}}'

# Direct string param tool
curl -X POST http://localhost:8000/appflowy/appflowy_get_folder \
  -H "Content-Type: application/json" \
  -d '{"workspace_id":"..."}'
```

## API Response Format

AppFlowy Cloud API는 모든 응답을 `{"data": {...}, "code": 0, "message": "..."}` 형식으로 래핑합니다.
`list_workspaces` 등 일부 tool은 `data["data"]`에서 배열을 꺼내야 하며, `data["workspaces"]` 키는 사용되지 않습니다.

## Known Gaps / Gotchas

- `requirements.txt` has only 3 deps (`mcp`, `httpx`, `pydantic`). `pyyaml` is needed for BRGS scripts but not listed here.
- `jwt_refresh.py` is NOT wired into the MCP server — it's dead code unless explicitly integrated.
- No `.gitignore` at repo root (only `.idea/.gitignore` exists). `token.json` and `__pycache__/` are not ignored.
- The migration script is basic: it creates pages in AppFlowy but does NOT migrate block-level content or database rows.
- French is the primary documentation language (README, mapping doc, comments).
- MCP server runs in **stdio mode** (reads JSON-RPC from stdin, writes to stdout) — standard for the MCP protocol.
- `POST /api/search` endpoint returns 404 on some self-hosted versions — AppFlowy search may not be available.
- `parent_view_id` is a **required** field when creating pages via the API — omitting it causes a 400 error. Use `get_folder` to find a space's `view_id` as the parent.
- `GET /api/workspace/{ws}/collab/{id}` (non-V1) is **deprecated** and returns 400 "Content type error". Always use the V1 endpoint with `?collab_type=N`.
- `POST /api/workspace/{ws}/invite` body must be a **JSON array** `[{email, role}]`, not a single object.
- `POST /api/search` is incorrect — search uses `GET /api/search/{workspace_id}?query=...&limit=...` with query string params (not JSON body), and requires the `appflowy_search` microservice to be running on port 4002.
