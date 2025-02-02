import pytest
from bson import ObjectId

from database import get_client


async def transactional_operations(session):
    await session.notes.insert_one(
        {
            "title": "title",
            "content": "content",
            "folder_id": ObjectId(),
            "created_at": "2021-01-01",
        },
        session=session,
    )

    await session.events.insert_one(
        {
            "aggregate_id": ObjectId(),
            "type": "NoteCreated",
            "payload": {"title": "title", "content": "content"},
            "created_at": "2021-01-01",
        },
        session=session,
    )

    raise Exception("Error")


@pytest.mark.asyncio
async def test__get_session__given_transaction__should_be_atomic(session):
    async with await get_client().start_session() as session:
        with pytest.raises(Exception):
            await session.with_transaction(lambda s: transactional_operations(s))

    notes = await session.notes.find().to_list()
    events = await session.events.find().to_list()

    assert not events, "Events should be rolled back"
    assert not notes, "Notes should be rolled back"
