"""Containers module."""

from dependency_injector import containers, providers

from .database import Database
from .repositories import LinkRepository
from .services import LinkService


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[".endpoints"])

    db = providers.Singleton(Database, db_url="sqlite:///./keys.db")

    link_repository = providers.Factory(
        LinkRepository,
        session_factory=db.provided.session,
    )

    link_service = providers.Factory(
        LinkService,
        link_repository=link_repository,
    )
