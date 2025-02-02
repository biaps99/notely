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
):
    folder = {"name": "Test Folder"}
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
    session, client
):
    folders = [
        {"name": f"Folder {i}", "created_at": f"2022-01-0{i}T00:00:00Z"}
        for i in range(5)
    ]
    await session.folders.insert_many(folders)

    response = await client.get(f"{API_PREFIX}?limit=2&offset=1")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "Folder 1"


@pytest.mark.asyncio
async def test__update_folder__given_valid_payload__should_return_ok(session, client):
    folder = {"name": "Old Name"}
    result = await session.folders.insert_one(folder)

    updated_payload = {"name": "Updated Name"}
    response = await client.put(
        f"{API_PREFIX}/{result.inserted_id}", json=updated_payload
    )

    assert response.status_code == 200
    updated_folder = await session.folders.find_one({"_id": result.inserted_id})
    assert updated_folder["name"] == "Updated Name"


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
