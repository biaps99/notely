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
    owner_id: str, folder: "dict[str, typing.Any]", session: "Session"
) -> "dict[str, typing.Any]":
    folder.update({"owner_id": owner_id})
    event_payload = copy.deepcopy(folder)
    document = {**folder, "created_at": get_now_utc()}
    insert_result = await session.folders.insert_one(document)
    if insert_result.inserted_id:
        await create_event(
            Event(
                aggregate_id=insert_result.inserted_id,
                type=FolderEventType.CREATED,
                payload=event_payload,
            ),
            session,
        )

    return document


async def get_folders(
    owner_id: str,
    session: "Session",
    limit: int = 20,
    offset: int = 0,
) -> "list[dict[str, typing.Any]]":
    return (
        await session.folders.find({"owner_id": owner_id})
        .sort("created_at")
        .limit(limit)
        .skip(offset)
        .to_list()
    )


async def update_folder(
    owner_id: str, folder_id: str, folder: "dict[str, typing.Any]", session: "Session"
) -> None:
    event_payload = copy.deepcopy(folder)
    update_result = await session.folders.update_one(
        {"_id": ObjectId(folder_id), "owner_id": owner_id},
        {"$set": {**folder, "last_updated_at": get_now_utc()}},
    )
    if update_result.modified_count:
        await create_event(
            Event(
                aggregate_id=folder_id,
                type=FolderEventType.UPDATED,
                payload=event_payload,
            ),
            session,
        )


async def delete_folder(owner_id: str, folder_id: str, session: "Session") -> None:
    delete_result = await session.folders.delete_one(
        {"_id": ObjectId(folder_id), "owner_id": owner_id}
    )
    if delete_result.deleted_count:
        await create_event(
            Event(aggregate_id=folder_id, type=FolderEventType.DELETED, payload={}),
            session,
        )


async def get_user_folder(
    user_id: str, folder_id: str, session: "Session"
) -> "typing.Optional[dict[str, typing.Any]]":
    return await session.folders.find_one(
        {"_id": ObjectId(folder_id), "owner_id": user_id}
    )
