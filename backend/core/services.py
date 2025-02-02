from typing import TYPE_CHECKING

from core.utils import get_now_utc

if TYPE_CHECKING:
    from database import Session
    from events import Event


async def get_events(session: "Session") -> "list[Event]":
    return await session.events.find().sort("created_at", -1).to_list()


async def create_event(event: "Event", session: "Session") -> None:
    await session.events.insert_one(
        {
            "aggregate_id": str(event.aggregate_id),
            "type": event.type.value,
            "payload": event.payload,
            "created_at": get_now_utc(),
        }
    )
