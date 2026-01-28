from __future__ import annotations

import uuid
from collections.abc import Iterable
from typing import Any

from pymongo import ASCENDING
from pymongo.database import Database

from specifai.workspaces.backend.data_models.workspace_models import (
    Workspace,
    WorkspaceCreate,
)
from specifai.workspaces.backend.data_repository.workspace_data_repository_base import (
    WorkspaceDataRepository,
)


class MongoWorkspaceDataRepository(WorkspaceDataRepository):
    def __init__(self, db: Database[dict[str, Any]]) -> None:
        self._db = db
        self._collection = db["workspaces"]

    def get_workspace_by_id(self, workspace_id: uuid.UUID) -> Workspace | None:
        doc = self._collection.find_one({"_id": str(workspace_id)})
        return self._doc_to_workspace(doc)

    def list_workspaces(
        self, *, owner_id: uuid.UUID | None, skip: int, limit: int
    ) -> tuple[list[Workspace], int]:
        query: dict[str, Any] = {}
        if owner_id is not None:
            query["owner_id"] = str(owner_id)
        count = self._collection.count_documents(query)
        cursor = self._collection.find(query).skip(skip).limit(limit)
        return self._cursor_to_workspaces(cursor), count

    def create_workspace(
        self, *, workspace_in: WorkspaceCreate, owner_id: uuid.UUID
    ) -> Workspace:
        workspace_data = workspace_in.model_dump()
        workspace = Workspace(**workspace_data, owner_id=owner_id)
        self._collection.insert_one(self._workspace_to_doc(workspace))
        return workspace

    def update_workspace(
        self, *, workspace: Workspace, update_data: dict[str, Any]
    ) -> Workspace:
        update_payload = self._serialize_workspace_update(update_data)
        if update_payload:
            self._collection.update_one(
                {"_id": str(workspace.id)}, {"$set": update_payload}
            )
        refreshed = self.get_workspace_by_id(workspace.id)
        if refreshed is None:
            raise ValueError("Workspace not found after update")
        return refreshed

    def delete_workspace(self, *, workspace: Workspace) -> None:
        self._collection.delete_one({"_id": str(workspace.id)})
        self._db["items"].delete_many({"workspace_id": str(workspace.id)})

    def get_or_create_default_workspace(self, *, owner_id: uuid.UUID) -> Workspace:
        doc = self._collection.find_one(
            {"owner_id": str(owner_id)},
            sort=[("name", ASCENDING)],
        )
        workspace = self._doc_to_workspace(doc)
        if workspace:
            return workspace
        workspace_in = WorkspaceCreate(name="Personal")
        return self.create_workspace(workspace_in=workspace_in, owner_id=owner_id)

    def _serialize_workspace_update(
        self, update_payload: dict[str, Any]
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        for key, value in update_payload.items():
            if value is None:
                payload[key] = None
            elif isinstance(value, uuid.UUID):
                payload[key] = str(value)
            else:
                payload[key] = value
        return payload

    def _workspace_to_doc(self, workspace: Workspace) -> dict[str, Any]:
        data = workspace.model_dump()
        data["_id"] = str(data.pop("id"))
        return self._serialize_workspace_update(data)

    def _doc_to_workspace(self, doc: dict[str, Any] | None) -> Workspace | None:
        if not doc:
            return None
        data = dict(doc)
        data["id"] = uuid.UUID(str(data.pop("_id")))
        if "owner_id" in data and data["owner_id"] is not None:
            data["owner_id"] = uuid.UUID(str(data["owner_id"]))
        return Workspace.model_validate(data)

    def _cursor_to_workspaces(
        self, cursor: Iterable[dict[str, Any]]
    ) -> list[Workspace]:
        workspaces: list[Workspace] = []
        for doc in cursor:
            workspace = self._doc_to_workspace(doc)
            if workspace:
                workspaces.append(workspace)
        return workspaces
