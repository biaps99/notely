from typing import TYPE_CHECKING

from database import get_session
from fastapi import APIRouter, Body, Depends, Query, status
from folders import constants, schemas, services

if TYPE_CHECKING:
    from database import Session

router = APIRouter(prefix=constants.API_PREFIX)


@router.post(
    "",
    description="Create a Folder",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.FolderRetrieve,
)
async def create_folder(
    folder: "schemas.FolderCreate" = Body(...),
    session: "Session" = Depends(get_session),
) -> "schemas.FolderRetrieve":
    return await session.with_transaction(
        lambda s: services.create_folder(folder.model_dump(), s)
    )


@router.get(
    "",
    description="Retrieve Folders given limit and offset",
    response_model=list[schemas.FolderRetrieve],
)
async def get_folders(
    limit: int = Query(20, ge=1),
    offset: int = Query(0, ge=0),
    session: "Session" = Depends(get_session),
) -> "list[schemas.FolderRetrieve]":
    return await services.get_folders(session, limit, offset)


@router.put("/{folder_id}", description="Update a given Folder")
async def update_folder(
    folder_id: str,
    folder: "schemas.FolderUpdate" = Body(...),
    session: "Session" = Depends(get_session),
) -> None:
    return await session.with_transaction(
        lambda s: services.update_folder(
            folder_id, folder.model_dump(exclude_unset=True), s
        )
    )


@router.delete(
    "/{folder_id}",
    description="Delete a given Folder",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_folder(
    folder_id: str,
    session: "Session" = Depends(get_session),
) -> None:
    await session.with_transaction(lambda s: services.delete_folder(folder_id, s))
