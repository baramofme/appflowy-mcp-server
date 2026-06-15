"""Data models for AppFlowy Cloud API."""
from typing import Any, Dict, List, Optional
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


class AFRole(str, Enum):
    OWNER = "Owner"
    MEMBER = "Member"
    GUEST = "Guest"


class AFViewType(str, Enum):
    DOCUMENT = "document"
    GRID = "grid"
    BOARD = "board"
    CALENDAR = "calendar"
    SPACE = "space"


class AuthLoginInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: str
    password: str


class CreateWorkspaceInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str


class CreatePageInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    workspace_id: str
    name: str
    parent_view_id: str
    view_type: AFViewType = AFViewType.DOCUMENT
    layout: int = 0
    page_data: Optional[Dict[str, Any]] = None


class GetPageInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    workspace_id: str
    view_id: str


class AppendBlockInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    workspace_id: str
    view_id: str
    blocks: List[Dict[str, Any]]


class UpdatePageNameInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    workspace_id: str
    view_id: str
    name: str


class SearchInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    query: str
    workspace_id: str
    limit: int = Field(10, ge=1, le=50)


class CollabGetInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    workspace_id: str
    object_id: str
    collab_type: int = 0
    json_format: bool = False


class InviteMemberInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    workspace_id: str
    email: str
    role: AFRole = AFRole.MEMBER


# --- New database models ---


class DatabaseListInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    workspace_id: str


class DatabaseFieldInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    workspace_id: str
    database_id: str


class CreateDatabaseFieldInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    workspace_id: str
    database_id: str
    name: str
    field_type: int
    type_option_data: Optional[Dict[str, Any]] = None


class DatabaseRowInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    workspace_id: str
    database_id: str


class CreateDatabaseRowInput(BaseModel):
    workspace_id: str
    database_id: str
    cells: Dict[str, Any]
    document: Optional[str] = None


class UpsertDatabaseRowInput(BaseModel):
    workspace_id: str
    database_id: str
    pre_hash: str
    cells: Dict[str, Any]
    document: Optional[str] = None


class DatabaseRowDetailInput(BaseModel):
    workspace_id: str
    database_id: str
    ids: str
    with_doc: Optional[bool] = None


class DatabaseRowUpdatedInput(BaseModel):
    workspace_id: str
    database_id: str
    after: Optional[str] = None


# --- New OAuth model ---


class OAuthTokenInput(BaseModel):
    code: str
    grant_type: str = "authorization_code"
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    redirect_uri: Optional[str] = None
    code_verifier: Optional[str] = None
