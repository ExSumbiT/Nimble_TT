"""Services module."""

from typing import Iterator

from .repositories import LinkRepository
from .models import Link


class LinkService:

    def __init__(self, link_repository: LinkRepository) -> None:
        self._repository: LinkRepository = link_repository

    def get_links(self) -> Iterator[Link]:
        return self._repository.get_all()

    def get_file_by_key(self, link_key: str) -> Link:
        return self._repository.get_by_key(link_key)

    def create_link(self, file) -> Link:
        return self._repository.add(file)
