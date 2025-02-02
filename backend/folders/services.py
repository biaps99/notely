import copy
import typing

from bson import ObjectId

from core.enums import FolderEventType
from core.events import Event
from core.services import create_event
from core.utils import get_now_utc

if typing.TYPE_CHECKING:
    from database import Session


async def create_folder(
    folder: "dict[str, typing.Any]", session: "Session"
) -> "dict[str, typing.Any]":
    event_payload = copy.deepcopy(folder)
    document = {**folder, "created_at": get_now_utc()}
    result = await session.folders.insert_one(document)
    await create_event(
        Event(
            aggregate_id=result.inserted_id,
            type=FolderEventType.CREATED,
            payload=event_payload,
        ),
        session,
    )
    return document


async def get_folders(
    session: "Session",
    limit: int = 20,
    offset: int = 0,
) -> "list[dict[str, typing.Any]]":
    return (
        await session.folders.find()
        .sort("created_at")
        .limit(limit)
        .skip(offset)
        .to_list()
    )


async def update_folder(
    folder_id: str, folder: "dict[str, typing.Any]", session: "Session"
) -> None:
    event_payload = copy.deepcopy(folder)
    await session.folders.update_one(
        {"_id": ObjectId(folder_id)},
        {"$set": {**folder, "last_updated_at": get_now_utc()}},
    )
    await create_event(
        Event(
            aggregate_id=folder_id, type=FolderEventType.UPDATED, payload=event_payload
        ),
        session,
    )


async def delete_folder(folder_id: str, session: "Session") -> None:
    await session.folders.delete_one({"_id": ObjectId(folder_id)})
    await create_event(
        Event(aggregate_id=folder_id, type=FolderEventType.DELETED, payload={}),
        session,
    )
