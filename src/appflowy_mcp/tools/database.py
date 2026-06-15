import json

from appflowy_mcp.mcp_instance import mcp
from appflowy_mcp.client import get_client
from appflowy_mcp.config import CHARACTER_LIMIT
from appflowy_mcp.models import (
    DatabaseListInput,
    DatabaseFieldInput,
    CreateDatabaseFieldInput,
    DatabaseRowInput,
    CreateDatabaseRowInput,
    UpsertDatabaseRowInput,
    DatabaseRowDetailInput,
    DatabaseRowUpdatedInput,
)


@mcp.tool(name="appflowy_list_databases", annotations={"readOnlyHint": True})
async def appflowy_list_databases(params: DatabaseListInput) -> str:
    client = get_client()
    raw = await client.request("GET", f"/api/workspace/{params.workspace_id}/database")
    inner = raw.get("data", raw)
    databases = inner if isinstance(inner, list) else inner.get("data", [])
    result = json.dumps(databases, indent=2)
    return result[:CHARACTER_LIMIT] if len(result) > CHARACTER_LIMIT else result


@mcp.tool(name="appflowy_get_database_fields", annotations={"readOnlyHint": True})
async def appflowy_get_database_fields(params: DatabaseFieldInput) -> str:
    client = get_client()
    raw = await client.request("GET", f"/api/workspace/{params.workspace_id}/database/{params.database_id}/fields")
    inner = raw.get("data", raw)
    fields = inner if isinstance(inner, list) else inner.get("data", [])
    result = json.dumps(fields, indent=2)
    return result[:CHARACTER_LIMIT] if len(result) > CHARACTER_LIMIT else result


@mcp.tool(name="appflowy_create_database_field", annotations={"readOnlyHint": False, "destructiveHint": False})
async def appflowy_create_database_field(params: CreateDatabaseFieldInput) -> str:
    client = get_client()
    body = {"name": params.name, "field_type": params.field_type}
    if params.type_option_data is not None:
        body["type_option_data"] = params.type_option_data
    data = await client.request(
        "POST",
        f"/api/workspace/{params.workspace_id}/database/{params.database_id}/fields",
        json=body,
    )
    return json.dumps(data, indent=2)


@mcp.tool(name="appflowy_list_database_rows", annotations={"readOnlyHint": True})
async def appflowy_list_database_rows(params: DatabaseRowInput) -> str:
    client = get_client()
    raw = await client.request("GET", f"/api/workspace/{params.workspace_id}/database/{params.database_id}/row")
    inner = raw.get("data", raw)
    rows = inner if isinstance(inner, list) else inner.get("data", [])
    result = json.dumps(rows, indent=2)
    return result[:CHARACTER_LIMIT] if len(result) > CHARACTER_LIMIT else result


@mcp.tool(name="appflowy_create_database_row", annotations={"readOnlyHint": False, "destructiveHint": False})
async def appflowy_create_database_row(params: CreateDatabaseRowInput) -> str:
    client = get_client()
    body = {"cells": params.cells}
    if params.document is not None:
        body["document"] = params.document
    data = await client.request(
        "POST",
        f"/api/workspace/{params.workspace_id}/database/{params.database_id}/row",
        json=body,
    )
    return json.dumps(data, indent=2)


@mcp.tool(name="appflowy_upsert_database_row", annotations={"readOnlyHint": False, "destructiveHint": False})
async def appflowy_upsert_database_row(params: UpsertDatabaseRowInput) -> str:
    client = get_client()
    body = {"pre_hash": params.pre_hash, "cells": params.cells}
    if params.document is not None:
        body["document"] = params.document
    data = await client.request(
        "PUT",
        f"/api/workspace/{params.workspace_id}/database/{params.database_id}/row",
        json=body,
    )
    return json.dumps(data, indent=2)


@mcp.tool(name="appflowy_get_database_row_details", annotations={"readOnlyHint": True})
async def appflowy_get_database_row_details(params: DatabaseRowDetailInput) -> str:
    client = get_client()
    query_params = {"ids": params.ids}
    if params.with_doc is not None:
        query_params["with_doc"] = params.with_doc
    raw = await client.request(
        "GET",
        f"/api/workspace/{params.workspace_id}/database/{params.database_id}/row/detail",
        params=query_params,
    )
    inner = raw.get("data", raw)
    details = inner if isinstance(inner, list) else inner.get("data", [])
    result = json.dumps(details, indent=2)
    return result[:CHARACTER_LIMIT] if len(result) > CHARACTER_LIMIT else result


@mcp.tool(name="appflowy_get_database_row_ids_updated", annotations={"readOnlyHint": True})
async def appflowy_get_database_row_ids_updated(params: DatabaseRowUpdatedInput) -> str:
    client = get_client()
    query_params = {}
    if params.after is not None:
        query_params["after"] = params.after
    raw = await client.request(
        "GET",
        f"/api/workspace/{params.workspace_id}/database/{params.database_id}/row/updated",
        params=query_params,
    )
    inner = raw.get("data", raw)
    items = inner if isinstance(inner, list) else inner.get("data", [])
    result = json.dumps(items, indent=2)
    return result[:CHARACTER_LIMIT] if len(result) > CHARACTER_LIMIT else result
