import pytest
from bson import ObjectId

from core.constants import API_PREFIX


@pytest.mark.asyncio
async def test__get_events__should_return_ok(client, session):
    event = {
        "aggregate_id": str(ObjectId()),
        "type": "NoteCreated",
        "payload": {
            "title": "title",
            "content": "content",
            "folder_id": str(ObjectId()),
        },
        "created_at": "2022-01-01T00:00:00Z",
    }
    result = await session.events.insert_one(event)

    response = await client.get(f"{API_PREFIX}/events")

    assert response.status_code == 200, response.text
    event.pop("_id")
    assert response.json() == [{**event, "id": str(result.inserted_id)}]
