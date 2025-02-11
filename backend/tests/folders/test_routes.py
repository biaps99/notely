import pytest
from bson import ObjectId, errors
from folders.constants import API_PREFIX


@pytest.mark.asyncio
async def test__create_folder__given_valid_payload__should_return_ok(client):
    payload = {"name": "Test Folder"}

    response = await client.post(API_PREFIX, json=payload)

    assert response.status_code == 201, response.text
    assert response.json() == {"name": payload["name"], "id": response.json()["id"]}


@pytest.mark.asyncio
async def test__create_folder__given_missing_fields__should_return_unprocessable(
    client,
):
    payload = {}

    response = await client.post(API_PREFIX, json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test__create_folder__given_excess_fields__should_return_ok(client):
    payload = {"name": "Test Folder", "extra": "field"}

    response = await client.post(API_PREFIX, json=payload)

    assert response.status_code == 201, response.text


@pytest.mark.asyncio
async def test__get_folders__given_no_folders__should_return_ok(client):
    response = await client.get(API_PREFIX)

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test__get_folders__given_folders__should_return_ok(
    session,
    client,
    auth_user,
):
    folder = {"name": "Test Folder", "owner_id": auth_user.user_id}
    result = await session.folders.insert_one(folder)

    response = await client.get(API_PREFIX)

    assert response.status_code == 200
    assert response.json() == [{"name": folder["name"], "id": str(result.inserted_id)}]


@pytest.mark.asyncio
async def test__get_folders_with_notes__given_no_folders__should_return_ok(client):
    response = await client.get(API_PREFIX)

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test__delete_folder__given_existent_folder__should_return_ok(
    session,
    client,
):
    result = await session.folders.insert_one({"name": "Test Folder"})

    response = await client.delete(f"{API_PREFIX}/{result.inserted_id}")

    assert response.status_code == 204


@pytest.mark.asyncio
async def test__get_folders__given_limit_and_offset__should_return_limited_results(
    session, client, auth_user
):
    folders = [
        {
            "name": f"Folder {i}",
            "created_at": f"2022-01-0{i}T00:00:00Z",
            "owner_id": auth_user.user_id,
        }
        for i in range(5)
    ]
    await session.folders.insert_many(folders)

    response = await client.get(f"{API_PREFIX}?limit=2&offset=1")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "Folder 1"


@pytest.mark.asyncio
async def test__update_folder__given_valid_payload__should_return_ok(
    session, client, auth_user
):
    folder = {"name": "Old Name", "owner_id": auth_user.user_id}
    result = await session.folders.insert_one(folder)

    updated_payload = {"name": "Updated Name"}
    response = await client.put(
        f"{API_PREFIX}/{result.inserted_id}", json=updated_payload
    )

    assert response.status_code == 200
    updated_folder = await session.folders.find_one({"_id": result.inserted_id})
    assert updated_folder["name"] == "Updated Name"
    assert updated_folder["last_updated_at"]


@pytest.mark.asyncio
async def test__update_folder__given_non_existent_folder__should_fail_silently(client):
    non_existent_id = str(ObjectId())
    updated_payload = {"name": "New Name"}

    response = await client.put(f"{API_PREFIX}/{non_existent_id}", json=updated_payload)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test__delete_folder__given_non_existent_folder__should_fail_silently(client):
    non_existent_id = str(ObjectId())

    response = await client.delete(f"{API_PREFIX}/{non_existent_id}")

    assert response.status_code == 204


@pytest.mark.asyncio
async def test__delete_folder__given_invalid_folder_id__should_return_bad_request(
    client,
):
    with pytest.raises(errors.InvalidId):
        response = await client.delete(f"{API_PREFIX}/invalid-id")
        assert response.status_code == 400


@pytest.mark.asyncio
async def test__create_note__given_valid_payload__should_return_ok(
    client, session, auth_user
):
    result = await session.folders.insert_one(
        {"name": "Test Folder", "owner_id": auth_user.user_id}
    )
    payload = {"title": "Test Note"}

    response = await client.post(
        f"{API_PREFIX}/{result.inserted_id}/notes", json=payload
    )

    assert response.status_code == 201, response.text


@pytest.mark.asyncio
async def test__create_note__given_missing_fields__should_return_unprocessable(
    client, session, auth_user
):
    result = await session.folders.insert_one(
        {"name": "Test Folder", "owner_id": auth_user.user_id}
    )

    response = await client.post(f"{API_PREFIX}/{result.inserted_id}/notes", json={})

    assert response.status_code == 422, response.text


@pytest.mark.asyncio
async def test__create_note__given_excess_fields__should_return_ok(
    client, session, auth_user
):
    result = await session.folders.insert_one(
        {"name": "Test Folder", "owner_id": auth_user.user_id}
    )
    payload = {
        "title": "Test Note",
        "content": "This is a test.",
        "extra": "field",
    }

    response = await client.post(
        f"{API_PREFIX}/{result.inserted_id}/notes", json=payload
    )

    assert response.status_code == 201, response.text


@pytest.mark.asyncio
async def test__get_notes__given_no_user_notes__should_return_ok(
    client, session, auth_user
):
    result = await session.folders.insert_one(
        {"name": "Test Folder", "owner_id": auth_user.user_id}
    )
    response = await client.get(f"{API_PREFIX}/{result.inserted_id}/notes")

    assert response.status_code == 200, response.text
    assert response.json() == []


@pytest.mark.asyncio
async def test__get_notes__given_notes__should_return_ok(client, session, auth_user):
    result = await session.folders.insert_one(
        {"name": "Test Folder", "owner_id": auth_user.user_id}
    )
    folder_id = str(result.inserted_id)
    note_payload = {
        "title": "Note",
        "content": "Content",
        "created_at": "2021-01-01T00:00:00Z",
        "folder_id": folder_id,
    }
    await session.notes.insert_one(note_payload)

    response = await client.get(f"{API_PREFIX}/{folder_id}/notes")

    assert response.status_code == 200, response.text
    res_json = response.json()
    assert len(res_json) == 1, "Should return list with one note"
    assert res_json[0]["title"] == note_payload["title"]
    assert res_json[0]["content"] == note_payload["content"]
    assert res_json[0]["folder_id"] == folder_id


@pytest.mark.asyncio
async def test__update_note__given_valid_payload__should_return_ok(
    client, session, auth_user
):
    result = await session.folders.insert_one(
        {"name": "Test Folder", "owner_id": auth_user.user_id}
    )
    folder_id = str(result.inserted_id)
    result = await session.notes.insert_one(
        {"title": "Note", "content": "Content", "folder_id": folder_id}
    )
    payload = {
        "title": "New Title for Note",
        "content": "New Content for Note.",
    }

    response = await client.put(
        f"{API_PREFIX}/{folder_id}/notes/{result.inserted_id}", json=payload
    )

    assert response.status_code == 200, response.text


@pytest.mark.asyncio
async def test__delete_note__given_existent_note__should_delete(
    client, session, auth_user
):
    result = await session.folders.insert_one(
        {"name": "Test Folder", "owner_id": auth_user.user_id}
    )
    folder_id = str(result.inserted_id)
    result = await session.notes.insert_one(
        {"title": "Note", "content": "Content", "folder_id": folder_id}
    )

    response = await client.delete(
        f"{API_PREFIX}/{folder_id}/notes/{result.inserted_id}"
    )

    assert response.status_code == 204, response.text


@pytest.mark.asyncio
async def test__get_notes__given_pagination__should_return_limited_results(
    client, session, auth_user
):
    result = await session.folders.insert_one(
        {"name": "Test Folder", "owner_id": auth_user.user_id}
    )
    folder_id = str(result.inserted_id)
    notes = [
        {
            "title": f"Note {i}",
            "content": "Content",
            "folder_id": folder_id,
            "last_updated_at": f"2022-01-1{i}T00:00:00Z",
        }
        for i in range(4)
    ]
    await session.notes.insert_many(notes)

    response = await client.get(f"{API_PREFIX}/{folder_id}/notes?limit=2&offset=1")

    assert response.status_code == 200, response.text
    res_json = response.json()
    assert len(res_json) == 2
    assert res_json[0]["title"] == "Note 1"
    assert res_json[1]["title"] == "Note 2"


@pytest.mark.asyncio
async def test__get_folder_notes__given_non_existent_folder__should_return_404(
    client,
):
    folder_id = str(ObjectId())

    response = await client.get(f"{API_PREFIX}/{folder_id}/notes")

    assert response.status_code == 404, response.text


@pytest.mark.asyncio
async def test__update_note__given_non_existent_note__should_return_404(client):
    folder_id = str(ObjectId())
    note_id = str(ObjectId())
    payload = {"title": "Updated Note", "content": "Updated Content"}

    response = await client.put(
        f"{API_PREFIX}/{folder_id}/notes/{note_id}", json=payload
    )

    assert response.status_code == 404, response.text


@pytest.mark.asyncio
async def test__delete_note__given_non_existent_note__should_return_404(client):
    note_id = str(ObjectId())
    folder_id = str(ObjectId())

    response = await client.delete(f"{API_PREFIX}/{folder_id}/notes/{note_id}")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test__create_note__given_non_existent_folder__should_return_404(client):
    folder_id = str(ObjectId())
    payload = {"title": "Test Note"}

    response = await client.post(f"{API_PREFIX}/{folder_id}/notes", json=payload)

    assert response.status_code == 404, response.text


@pytest.mark.asyncio
async def test__get_notes__given_unauthorized_folder__should_return_404(client):
    folder_id = str(ObjectId())

    response = await client.get(f"{API_PREFIX}/{folder_id}/notes")

    assert response.status_code == 404, response.text


@pytest.mark.asyncio
async def test__update_note__given_unauthorized_folder__should_return_404(client):
    folder_id = str(ObjectId())
    note_id = str(ObjectId())
    payload = {"title": "Updated Note", "content": "Updated Content"}

    response = await client.put(
        f"{API_PREFIX}/{folder_id}/notes/{note_id}", json=payload
    )

    assert response.status_code == 404, response.text


@pytest.mark.asyncio
async def test__delete_note__given_unauthorized_folder__should_return_404(client):
    folder_id = str(ObjectId())
    note_id = str(ObjectId())

    response = await client.delete(f"{API_PREFIX}/{folder_id}/notes/{note_id}")

    assert response.status_code == 404, response.text


@pytest.mark.asyncio
async def test__get_notes__given_pagination_exceeding_notes__should_return_correct_count(
    client, session, auth_user
):
    result = await session.folders.insert_one(
        {"name": "Test Folder", "owner_id": auth_user.user_id}
    )
    folder_id = str(result.inserted_id)
    notes = [
        {
            "title": f"Note {i}",
            "content": "Content",
            "folder_id": folder_id,
            "last_updated_at": f"2022-01-1{i}T00:00:00Z",
        }
        for i in range(2)
    ]
    await session.notes.insert_many(notes)

    response = await client.get(f"{API_PREFIX}/{folder_id}/notes?limit=5")

    assert response.status_code == 200, response.text
    res_json = response.json()
    assert len(res_json) == 2, "Should return only available notes"
