"""Models module."""

from sqlalchemy import Column, String
from fastapi_utils.guid_type import GUID
import uuid

from .database import Base


class Link(Base):

    __tablename__ = "files"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    key = Column(String, unique=True, nullable=False)
    value = Column(String, nullable=False)
