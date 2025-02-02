from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

    from bson import ObjectId

    from enums import EventType


@dataclass(frozen=True)
class Event:
    aggregate_id: "ObjectId"
    payload: "dict[str, Any]"
    type: "EventType"
