import pytest
from bson import ObjectId

from core import services


@pytest.mark.asyncio
async def test__get_events__given_no_events__should_return(session):
    results = await services.get_events(session)

    assert len(results) == 0, "Should return empty list"


@pytest.mark.asyncio
async def test__get_events__given_events__should_return_events(
    session,
):
    event = {
        "aggregate_id": ObjectId(),
        "type": "NoteCreated",
        "payload": {"title": "title", "content": "content", "folder_id": ObjectId()},
    }
    result = await session.events.insert_one(event)

    results = await services.get_events(session)

    assert len(results) == 1, "Should return list with one event"
    assert results[0]["aggregate_id"] == event["aggregate_id"]
    assert results[0]["type"] == event["type"]
    assert results[0]["payload"] == event["payload"]
    assert results[0]["_id"] == result.inserted_id
