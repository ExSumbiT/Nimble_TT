"""Endpoints module."""

from fastapi import APIRouter, Depends, Response, UploadFile, status
from fastapi.responses import FileResponse, StreamingResponse
from dependency_injector.wiring import inject, Provide

from .container import Container
from .services import LinkService
from .repositories import NotFoundError

router = APIRouter()


@router.get("/links")
@inject
def get_list(
        link_service: LinkService = Depends(Provide[Container.link_service]),
):
    return link_service.get_links()


@router.get("/read/{link_key}")
@inject
def get_by_key(
        link_key: str,
        link_service: LinkService = Depends(Provide[Container.link_service]),
):
    try:
        filename, file_binary_stream = link_service.get_file_by_key(link_key)
        headers = {
            'Content-Disposition': f'attachment; filename="{filename}"'}
        return Response(file_binary_stream, headers=headers)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.put("/write", status_code=status.HTTP_201_CREATED)
@inject
def add(file: UploadFile,
        link_service: LinkService = Depends(Provide[Container.link_service]),
        ):
    return link_service.create_link(file)
