from contextlib import AbstractContextManager
from typing import Callable, Iterator
import uuid
from transliterate import translit, exceptions

from sqlalchemy.orm import Session

from .models import Link
from .dropbox_storage import Storage


class LinkRepository:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory
        self.storage = Storage()

    def get_all(self) -> Iterator[Link]:
        """returns all Link model objects"""

        with self.session_factory() as session:
            return session.query(Link).all()

    def get_by_key(self, link_key: str) -> Link:
        """loads a file from storage, returns its name and data stream"""

        with self.session_factory() as session:
            link = session.query(Link).filter(Link.key == link_key).first()
            if not link:
                raise LinkNotFoundError(link_key)
            filename, stream = self.storage.download_file(link.value)
            # Cyrillic transcript in the file name
            try:
                filename = translit(
                    ''.join(filename.split('|')[1:]), reversed=True)
            # if the file name is missing Cyrillic
            except exceptions.LanguageDetectionError:
                pass
            return filename, stream

    def add(self, file) -> Link:
        """uploads a file to storage, creates and returns a Link model object"""

        key = str(uuid.uuid4())
        value = key + '|' + file.filename
        self.storage.upload_file(file.file.read(), value)
        with self.session_factory() as session:
            link = Link(key=key, value=value)
            session.add(link)
            session.commit()
            session.refresh(link)
            return link


class NotFoundError(Exception):

    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f"{self.entity_name} not found, id: {entity_id}")


class LinkNotFoundError(NotFoundError):

    entity_name: str = "Link"
