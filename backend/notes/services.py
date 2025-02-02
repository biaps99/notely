import copy
import typing

from bson import ObjectId

from core.enums import NoteEventType
from core.events import Event
from core.services import create_event
from core.utils import get_now_utc

if typing.TYPE_CHECKING:
    from database import Session


async def create_note(
    note: "dict[str, typing.Any]", session: "Session"
) -> "dict[str, typing.Any]":
    event_payload = copy.deepcopy(note)
    document = {**note, "created_at": get_now_utc(), "last_updated_at": get_now_utc()}
    result = await session.notes.insert_one(document)
    await create_event(
        Event(
            aggregate_id=result.inserted_id,
            type=NoteEventType.CREATED,
            payload=event_payload,
        ),
        session,
    )
    return document


async def get_notes(
    session: "Session",
    limit: int = 20,
    offset: int = 0,
) -> "list[dict[str, typing.Any]]":
    return (
        await session.notes.find()
        .sort("last_updated_at")
        .limit(limit)
        .skip(offset)
        .to_list()
    )


async def get_folder_notes(
    folder_id: str,
    session: "Session",
    limit: int = 20,
    offset: int = 0,
) -> "list[dict[str, typing.Any]]":
    return (
        await session.notes.find(
            {"folder_id": folder_id},
        )
        .sort("last_updated_at")
        .limit(limit)
        .skip(offset)
        .to_list()
    )


async def update_note(
    note_id: str, note: "dict[str, typing.Any]", session: "Session"
) -> "dict[str, typing.Any]":
    event_payload = copy.deepcopy(note)
    document = {**note, "last_updated_at": get_now_utc()}
    await session.notes.update_one({"_id": ObjectId(note_id)}, {"$set": document})
    await create_event(
        Event(aggregate_id=note_id, type=NoteEventType.UPDATED, payload=event_payload),
        session,
    )
    return document


async def delete_note(note_id: str, session: "Session") -> None:
    await session.notes.delete_one({"_id": ObjectId(note_id)})
    await create_event(
        Event(aggregate_id=note_id, type=NoteEventType.DELETED, payload={}), session
    )
