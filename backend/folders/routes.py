from typing import TYPE_CHECKING

from fastapi import (
    APIRouter,
    Body,
    Depends,
    Query,
    status,
    HTTPException,
    UploadFile,
    File,
)
from file_storage import upload
from database import get_session
from folders import constants, schemas, services
from notes import schemas as note_schemas, services as note_services
from core.auth import get_auth_user

if TYPE_CHECKING:
    from database import Session
    from core.auth import AuthUser

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
    auth_user: "AuthUser" = Depends(get_auth_user),
) -> "schemas.FolderRetrieve":
    return await session.with_transaction(
        lambda s: services.create_folder(auth_user.user_id, folder.model_dump(), s)
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
    auth_user: "AuthUser" = Depends(get_auth_user),
) -> "list[schemas.FolderRetrieve]":
    return await services.get_folders(auth_user.user_id, session, limit, offset)


@router.put("/{folder_id}", description="Update a given Folder")
async def update_folder(
    folder_id: str,
    folder: "schemas.FolderUpdate" = Body(...),
    session: "Session" = Depends(get_session),
    auth_user: "AuthUser" = Depends(get_auth_user),
) -> None:
    return await session.with_transaction(
        lambda s: services.update_folder(
            auth_user.user_id, folder_id, folder.model_dump(exclude_unset=True), s
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
    auth_user: "AuthUser" = Depends(get_auth_user),
) -> None:
    await session.with_transaction(
        lambda s: services.delete_folder(auth_user.user_id, folder_id, s)
    )


@router.post(
    "/{folder_id}/notes",
    description="Create a Note in a given Folder",
    status_code=status.HTTP_201_CREATED,
    response_model=note_schemas.NoteRetrieve,
)
async def create_note(
    folder_id: str,
    note: "note_schemas.NoteCreate" = Body(...),
    session: "Session" = Depends(get_session),
    auth_user: "AuthUser" = Depends(get_auth_user),
) -> "note_schemas.NoteRetrieve":
    if not await services.get_user_folder(auth_user.user_id, folder_id, session):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return await session.with_transaction(
        lambda s: note_services.create_note(folder_id, note.model_dump(), s)
    )


@router.get(
    "/{folder_id}/notes",
    description="Retrieve all Notes of a given Folder",
    response_model=list[note_schemas.NoteRetrieve],
)
async def get_notes(
    folder_id: str,
    limit: int = Query(20, ge=1),
    offset: int = Query(0, ge=0),
    session: "Session" = Depends(get_session),
    auth_user: "AuthUser" = Depends(get_auth_user),
) -> list["note_schemas.NoteRetrieve"]:
    if not await services.get_user_folder(auth_user.user_id, folder_id, session):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return await note_services.get_folder_notes(folder_id, session, limit, offset)


@router.put(
    "/{folder_id}/notes/{note_id}",
    description="Update a given Note in a given Folder",
    response_model=note_schemas.NoteUpdate,
)
async def update_note(
    folder_id: str,
    note_id: str,
    note: "note_schemas.NoteUpdate" = Body(...),
    session: "Session" = Depends(get_session),
    auth_user: "AuthUser" = Depends(get_auth_user),
) -> "note_schemas.NoteUpdate":
    if not await services.get_user_folder(auth_user.user_id, folder_id, session):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return await session.with_transaction(
        lambda s: note_services.update_note(
            note_id, folder_id, note.model_dump(exclude_unset=True), s
        )
    )


@router.post(
    "/{folder_id}/notes/{note_id}/images",
    description="Uploads an image from a given Note in a given Folder",
    response_model=note_schemas.ImageUpload,
)
async def upload_image(
    folder_id: str,
    note_id: str,
    image_file: "UploadFile" = File(...),
    auth_user: "AuthUser" = Depends(get_auth_user),
    session: "Session" = Depends(get_session),
) -> "note_schemas.ImageUpload":
    if not await services.get_user_folder(
        auth_user.user_id, folder_id, session
    ) or not await note_services.get_folder_note(note_id, folder_id, session):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    upload_path = await upload(auth_user.user_id, image_file)
    return {"path": upload_path}


@router.delete(
    "/{folder_id}/notes/{note_id}",
    description="Delete a given Note in a given Folder",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_note(
    folder_id: str,
    note_id: str,
    session: "Session" = Depends(get_session),
    auth_user: "AuthUser" = Depends(get_auth_user),
) -> None:
    if not await services.get_user_folder(auth_user.user_id, folder_id, session):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await session.with_transaction(
        lambda s: note_services.delete_note(note_id, folder_id, s)
    )
