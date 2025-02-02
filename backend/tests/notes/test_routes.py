import pytest
from bson import ObjectId
from notes.constants import API_PREFIX


@pytest.mark.asyncio
async def test__create_note__given_valid_payload__should_return_ok(client):
    payload = {
        "title": "Test Note",
        "folder_id": str(ObjectId()),
    }

    response = await client.post(API_PREFIX, json=payload)

    assert response.status_code == 201, response.text


@pytest.mark.asyncio
async def test__create_note__given_missing_fields__should_return_unprocessable(client):
    payload = {"title": "Test Note"}

    response = await client.post(API_PREFIX, json=payload)

    assert response.status_code == 422, response.text


@pytest.mark.asyncio
async def test__create_note__given_excess_fields__should_return_ok(client):
    payload = {
        "title": "Test Note",
        "content": "This is a test.",
        "extra": "field",
        "folder_id": str(ObjectId()),
    }

    response = await client.post(API_PREFIX, json=payload)

    assert response.status_code == 201, response.text


@pytest.mark.asyncio
async def test__get_notes__given_no_notes__should_return_ok(client):
    response = await client.get(API_PREFIX)

    assert response.status_code == 200, response.text
    assert response.json() == []


@pytest.mark.asyncio
async def test__get_notes__given_notes__should_return_ok(client, session):
    note_payload = {
        "title": "Note",
        "content": "Content",
        "created_at": "2021-01-01T00:00:00Z",
        "folder_id": str(ObjectId()),
    }
    await session.notes.insert_one(note_payload)

    response = await client.get(API_PREFIX)

    assert response.status_code == 200, response.text
    res_json = response.json()
    assert len(res_json) == 1, "Should return list with one note"
    assert res_json[0]["title"] == note_payload["title"]
    assert res_json[0]["content"] == note_payload["content"]
    assert res_json[0]["folder_id"] == str(note_payload["folder_id"])


@pytest.mark.asyncio
async def test__update_note__given_valid_payload__should_return_ok(client, session):
    result = await session.notes.insert_one({"title": "Note", "content": "Content"})
    payload = {
        "title": "New Title for Note",
        "content": "New Content for Note.",
    }

    response = await client.put(f"{API_PREFIX}/{result.inserted_id}", json=payload)

    assert response.status_code == 200, response.text


@pytest.mark.asyncio
async def test__delete_note__given_existent_note__should_delete(client, session):
    result = await session.notes.insert_one({"title": "Note", "content": "Content"})

    response = await client.delete(f"{API_PREFIX}/{result.inserted_id}")

    assert response.status_code == 204, response.text


@pytest.mark.asyncio
async def test__get_notes__given_pagination__should_return_limited_results(
    client, session
):
    notes = [
        {
            "title": f"Note {i}",
            "content": "Content",
            "folder_id": str(ObjectId()),
            "last_updated_at": f"2022-01-1{i}T00:00:00Z",
        }
        for i in range(4)
    ]
    await session.notes.insert_many(notes)

    response = await client.get(f"{API_PREFIX}?limit=2&offset=1")

    assert response.status_code == 200, response.text
    res_json = response.json()
    assert len(res_json) == 2
    assert res_json[0]["title"] == "Note 1"
    assert res_json[1]["title"] == "Note 2"


@pytest.mark.asyncio
async def test__get_folder_notes__given_existing_folder__should_return_notes(
    client, session
):
    folder_id = str(ObjectId())
    notes = [
        {"title": "Note 1", "content": "Content 1", "folder_id": folder_id},
        {"title": "Note 2", "content": "Content 2", "folder_id": folder_id},
    ]
    await session.notes.insert_many(notes)

    response = await client.get(f"{API_PREFIX}/{folder_id}")

    assert response.status_code == 200, response.text
    res_json = response.json()
    assert len(res_json) == 2
    assert res_json[0]["folder_id"] == folder_id
    assert res_json[1]["folder_id"] == folder_id


@pytest.mark.asyncio
async def test__get_folder_notes__given_non_existent_folder__should_return_empty(
    client,
):
    folder_id = str(ObjectId())

    response = await client.get(f"{API_PREFIX}/{folder_id}")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test__update_note__given_non_existent_note__should_fail_silently(client):
    note_id = str(ObjectId())
    payload = {"title": "Updated Note", "content": "Updated Content"}

    response = await client.put(f"{API_PREFIX}/{note_id}", json=payload)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test__delete_note__given_non_existent_note__should_fail_silently(client):
    note_id = str(ObjectId())

    response = await client.delete(f"{API_PREFIX}/{note_id}")

    assert response.status_code == 204


@pytest.mark.asyncio
async def test__create_note__should_assign_to_correct_folder(client, session):
    folder_id = str(ObjectId())
    payload = {
        "title": "Folder Test Note",
        "content": "Some content",
        "folder_id": folder_id,
    }

    response = await client.post(API_PREFIX, json=payload)

    assert response.status_code == 201
    note = await session.notes.find_one({"title": payload["title"]})

    assert note is not None, "Note was not created"
    assert note["folder_id"] == folder_id


@pytest.mark.asyncio
async def test__update_note__given_partial_payload__should_update_correctly(
    client, session
):
    note_id = await session.notes.insert_one(
        {"title": "Original Note", "content": "Original Content"}
    )
    payload = {"content": "Updated Content"}

    response = await client.put(f"{API_PREFIX}/{note_id.inserted_id}", json=payload)

    assert response.status_code == 200
    updated_note = await session.notes.find_one({"_id": note_id.inserted_id})
    assert updated_note["title"] == "Original Note"
    assert updated_note["content"] == "Updated Content"
