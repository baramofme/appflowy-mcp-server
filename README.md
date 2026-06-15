# AppFlowy MCP Server

Serveur MCP pour interagir avec AppFlowy Cloud — remplacement de Notion.

## Outils MCP

| Outil | Description | Read-only |
|-------|-------------|-----------|
| `appflowy_auth_login` | Authentification GoTrue JWT | ❌ |
| `appflowy_list_workspaces` | Liste les workspaces | ✅ |
| `appflowy_create_workspace` | Crée un workspace | ❌ |
| `appflowy_get_folder` | Structure hiérarchique du workspace | ✅ |
| `appflowy_create_page` | Crée une page/database | ❌ |
| `appflowy_get_page` | Récupère le contenu d'une page | ✅ |
| `appflowy_append_block` | Ajoute des blocs à une page | ❌ |
| `appflowy_update_page_name` | Renomme une page | ❌ |
| `appflowy_search` | Recherche full-text | ✅ |
| `appflowy_get_collab` | Objet collaboratif | ✅ |
| `appflowy_list_members` | Membres du workspace | ✅ |
| `appflowy_invite_member` | Invite un membre | ❌ |
| `appflowy_health_check` | Vérifie la connectivité | ✅ |
| `appflowy_list_databases` | Liste les bases de données | ✅ |
| `appflowy_get_database_fields` | Champs d'une base de données | ✅ |
| `appflowy_create_database_field` | Crée un champ dans une base | ❌ |
| `appflowy_list_database_rows` | Liste les lignes d'une base | ✅ |
| `appflowy_create_database_row` | Crée une ligne | ❌ |
| `appflowy_upsert_database_row` | Crée ou met à jour une ligne | ❌ |
| `appflowy_get_database_row_details` | Détails d'une ligne | ✅ |
| `appflowy_get_database_row_ids_updated` | Lignes récemment modifiées | ✅ |
| `appflowy_auth_oauth_token` | Échange code OAuth contre token | ✅ |

## Configuration

```bash
export APPFLOWY_BASE_URL="https://api.appflowy.io"  # ou votre instance self-hosted
export APPFLOWY_TOKEN="votre_jwt_token"
```

## Migration Notion → AppFlowy

```bash
python src/migrate_notion_to_appflowy.py <workspace_id>
```

## Fichiers

- `src/appflowy_mcp.py` — Point d'entrée mince (compatibilité mcp.json)
- `src/appflowy_mcp/` — Package MCP server (22 outils)
  - `config.py` — Constantes de configuration
  - `client.py` — Client HTTP (AppFlowyClient)
  - `models.py` — Modèles Pydantic
  - `mcp_instance.py` — Instance FastMCP
  - `tools/` — Modules d'outils MCP
- `src/migrate_notion_to_appflowy.py` — Script de migration
- `NOTION-TO-APPFLOWY-MAPPING.md` — Mapping des concepts
- `requirements.txt` — Dépendances Python
- `mcp.json` — Configuration MCP
