import uuid
from typing import List, Type

import dramatiq
from sqlalchemy.exc import DBAPIError

from fief.logger import logger
from fief.repositories import (
    AuthorizationCodeRepository,
    LoginSessionRepository,
    OAuthSessionRepository,
    RefreshTokenRepository,
    RegistrationSessionRepository,
    SessionTokenRepository,
    WorkspaceRepository,
)
from fief.repositories.base import ExpiresAtRepositoryProtocol
from fief.services.workspace_db import WorkspaceDatabase
from fief.tasks.base import TaskBase

repository_classes: List[Type[ExpiresAtRepositoryProtocol]] = [
    AuthorizationCodeRepository,
    LoginSessionRepository,
    OAuthSessionRepository,
    RefreshTokenRepository,
    RegistrationSessionRepository,
    SessionTokenRepository,
]


class CleanupWorkspaceTask(TaskBase):
    __name__ = "cleanup_workspace"

    async def run(self, workspace_id: str):
        latest_revision = WorkspaceDatabase().get_latest_revision()
        workspace = await self._get_workspace(uuid.UUID(workspace_id))
        if workspace.alembic_revision != latest_revision:
            return

        try:
            async with self.get_workspace_session(workspace) as workspace_session:
                for repository_class in repository_classes:
                    repository = repository_class(workspace_session)
                    await repository.delete_expired()
        except ConnectionError:
            logger.warning(
                "Could not connect to workspace", workspace_id=str(workspace.id)
            )
        except DBAPIError as e:
            logger.warning(
                "An error occured while querying workspace",
                workspace_id=str(workspace.id),
                message=str(e),
            )


cleanup_workspace = dramatiq.actor(CleanupWorkspaceTask(), max_retries=0)


class CleanupTask(TaskBase):
    __name__ = "cleanup"

    async def run(self):
        async with self.get_main_session() as session:
            workspace_repository = WorkspaceRepository(session)
            workspaces = await workspace_repository.all()
            for workspace in workspaces:
                self.send_task(cleanup_workspace, workspace_id=str(workspace.id))


cleanup = dramatiq.actor(CleanupTask())
