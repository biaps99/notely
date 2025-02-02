from typing import TYPE_CHECKING

from fastapi import APIRouter, Body, Depends, Query, status

from database import get_session
from notes import constants, schemas, services

if TYPE_CHECKING:
    from database import Session

router = APIRouter(prefix=constants.API_PREFIX)


@router.post(
    "",
    description="Create a Note",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.NoteRetrieve,
)
async def create_note(
    note: "schemas.NoteCreate" = Body(...), session: "Session" = Depends(get_session)
) -> "schemas.NoteRetrieve":
    return await session.with_transaction(
        lambda s: services.create_note(note.model_dump(), s)
    )


@router.get(
    "", description="Retrieve all Notes", response_model=list[schemas.NoteRetrieve]
)
async def get_notes(
    limit: int = Query(20, ge=1),
    offset: int = Query(0, ge=0),
    session: "Session" = Depends(get_session),
) -> list["schemas.NoteRetrieve"]:
    return await services.get_notes(session, limit, offset)


@router.get(
    "/{folder_id}",
    description="Retrieve all Notes of a given Folder",
    response_model=list[schemas.NoteRetrieve],
)
async def get_folder_notes(
    folder_id: str,
    limit: int = Query(20, ge=1),
    offset: int = Query(0, ge=0),
    session: "Session" = Depends(get_session),
) -> list["schemas.NoteRetrieve"]:
    return await services.get_folder_notes(folder_id, session, limit, offset)


@router.put(
    "/{note_id}", description="Update a given Note", response_model=schemas.NoteUpdate
)
async def update_note(
    note_id: str,
    note: "schemas.NoteUpdate" = Body(...),
    session: "Session" = Depends(get_session),
) -> "schemas.NoteUpdate":
    return await session.with_transaction(
        lambda s: services.update_note(note_id, note.model_dump(exclude_unset=True), s)
    )


@router.delete(
    "/{note_id}",
    description="Delete a given Note",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_note(
    note_id: str,
    session: "Session" = Depends(get_session),
) -> None:
    await session.with_transaction(lambda s: services.delete_note(note_id, s))
