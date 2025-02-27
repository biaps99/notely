import pytest
from bson import ObjectId, errors

from notes import services


@pytest.mark.asyncio
async def test__create_note__should_create_note(session):
    folder_id = ObjectId()
    payload = {
        "title": "Test Note",
        "content": "This is a test.",
    }

    await services.create_note(folder_id, payload, session)

    note = await session.notes.find_one({"title": payload["title"]})

    assert note, "Note was not created"
    assert note["content"] == payload["content"]
    assert note["folder_id"] == folder_id


@pytest.mark.asyncio
async def test__update_note__given_new_title__should_update(session):
    folder_id = ObjectId()
    note_payload = {"title": "Note", "content": "Content", "folder_id": folder_id}
    result = await session.notes.insert_one(note_payload)
    update_payload = {
        "title": "New Note",
    }

    await services.update_note(result.inserted_id, folder_id, update_payload, session)

    updated_note = await session.notes.find_one({"_id": result.inserted_id})

    assert updated_note["title"] == update_payload["title"]


@pytest.mark.asyncio
async def test__update_note__given_new_content_title__should_update(
    session,
):
    folder_id = ObjectId()
    note = {"title": "Note", "content": "Content", "folder_id": folder_id}
    result = await session.notes.insert_one(note)
    payload = {"title": "New Note", "content": "New Content"}

    await services.update_note(result.inserted_id, folder_id, payload, session)

    updated_note = await session.notes.find_one({"_id": result.inserted_id})

    assert updated_note["title"] == payload["title"]
    assert updated_note["content"] == payload["content"]


@pytest.mark.asyncio
async def test__delete_note__should_soft_delete(session):
    folder_id = ObjectId()
    result = await session.notes.insert_one(
        {"title": "Note", "content": "Content", "folder_id": folder_id}
    )

    await services.delete_note(result.inserted_id, folder_id, session)

    deleted_note = await session.notes.find_one({"_id": result.inserted_id})

    assert not deleted_note, "Note was not deleted"


@pytest.mark.asyncio
async def test__get_folder_notes__should_return(
    session,
):
    result = await session.folders.insert_one({"name": "Test Folder"})
    await session.notes.insert_one(
        {"title": "Note", "content": "Content", "folder_id": result.inserted_id}
    )
    note = {"title": "Note 2", "content": "Content 2", "folder_id": ObjectId()}
    await session.notes.insert_one(note)

    notes = await services.get_folder_notes(result.inserted_id, session)

    assert len(notes) == 1
    assert notes[0]["title"] == "Note"
    assert notes[0]["content"] == "Content"


@pytest.mark.asyncio
async def test__get_folder_notes__should_exclude_soft_deleted(session):
    result_folder = await session.folders.insert_one({"name": "Test Folder"})
    result_note = await session.notes.insert_one(
        {"title": "Note", "content": "Content", "folder_id": result_folder.inserted_id}
    )
    await services.delete_note(
        result_note.inserted_id, result_folder.inserted_id, session
    )

    notes = await services.get_folder_notes(result_folder.inserted_id, session)

    assert len(notes) == 0


@pytest.mark.asyncio
async def test__create_note__without_optional_fields__should_succeed(session):
    payload = {"title": "Test Note"}
    folder_id = ObjectId()

    created_note = await services.create_note(folder_id, payload, session)

    assert created_note["title"] == payload["title"]
    assert created_note["folder_id"] == payload["folder_id"]
    assert "content" not in created_note


@pytest.mark.asyncio
async def test__update_note__with_empty_payload__should_not_remove_existing_fields(
    session,
):
    folder_id = ObjectId()
    note = {
        "title": "Original Note",
        "content": "Original Content",
        "folder_id": folder_id,
    }
    result = await session.notes.insert_one(note)

    await services.update_note(result.inserted_id, folder_id, {}, session)

    updated_note = await session.notes.find_one({"_id": result.inserted_id})

    assert updated_note["title"] == note["title"]
    assert updated_note["content"] == note["content"]


@pytest.mark.asyncio
async def test__create_note__should_trigger_create_event(session):
    payload = {"title": "Test Note"}
    folder_id = ObjectId()

    result = await services.create_note(folder_id, payload, session)

    events = await session.events.find().to_list()

    assert len(events) == 1
    assert events[0]["type"] == "NOTE_CREATED"
    assert events[0]["aggregate_id"] == str(result["_id"])


@pytest.mark.asyncio
async def test__update_note__should_trigger_update_event(session):
    folder_id = ObjectId()
    note = {"title": "Note", "content": "Content", "folder_id": folder_id}
    result = await session.notes.insert_one(note)
    update_payload = {"title": "Updated Note"}

    await services.update_note(result.inserted_id, folder_id, update_payload, session)

    events = await session.events.find().to_list()

    assert len(events) == 1
    assert events[0]["type"] == "NOTE_UPDATED"
    assert events[0]["aggregate_id"] == str(result.inserted_id)


@pytest.mark.asyncio
async def test__delete_note__should_trigger_delete_event(session):
    folder_id = ObjectId()
    note = {"title": "Note", "content": "Content", "folder_id": folder_id}
    result = await session.notes.insert_one(note)

    await services.delete_note(result.inserted_id, folder_id, session)

    events = await session.events.find().to_list()

    assert len(events) == 1
    assert events[0]["type"] == "NOTE_DELETED"
    assert events[0]["aggregate_id"] == str(result.inserted_id)


@pytest.mark.asyncio
async def test__update_note__with_invalid_id__should_raise(session):
    invalid_id = "not_a_valid_object_id"
    payload = {"title": "New Title"}

    with pytest.raises(errors.InvalidId):
        await services.update_note(invalid_id, ObjectId(), payload, session)


@pytest.mark.asyncio
async def test__delete_note__with_invalid_id__should_raise(session):
    invalid_id = "not_a_valid_object_id"

    with pytest.raises(errors.InvalidId):
        await services.delete_note(invalid_id, ObjectId(), session)


@pytest.mark.asyncio
async def test__get_folder_notes__with_pagination__should_return_limited_results(
    session,
):
    folder_id = ObjectId()
    notes = [
        {
            "title": f"Note {i}",
            "content": f"Content {i}",
            "folder_id": folder_id,
            "last_updated_at": f"2022-01-{i}T00:00:00Z",
        }
        for i in range(5)
    ]
    await session.notes.insert_many(notes)

    results = await services.get_folder_notes(folder_id, session, limit=2, offset=2)

    assert len(results) == 2
    assert results[0]["title"] == "Note 2"
    assert results[1]["title"] == "Note 3"
