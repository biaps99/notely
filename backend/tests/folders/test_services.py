import pytest
from bson import ObjectId

from core.enums import FolderEventType
from folders import services


@pytest.mark.asyncio
async def test__create_folder__should_create(session):
    payload = {"name": "Test Folder"}

    await services.create_folder(owner_id="user123", folder=payload, session=session)

    folder = await session.folders.find_one({"name": payload["name"]})

    assert folder, "Folder was not created"
    assert folder["name"] == payload["name"]
    assert folder["owner_id"] == "user123"


@pytest.mark.asyncio
async def test__get_folders__given_no_folders__should_return(session):
    folders = await services.get_folders(owner_id="user123", session=session)

    assert folders == []


@pytest.mark.asyncio
async def test__get_folders__given_folders__should_return(session):
    result = await session.folders.insert_one(
        {"name": "Test Folder", "owner_id": "user123"}
    )

    folders = await services.get_folders(owner_id="user123", session=session)

    assert len(folders) == 1
    assert folders[0]["_id"] == result.inserted_id


@pytest.mark.asyncio
async def test__get_folders__given_no_user_folders__should_return(session):
    await session.folders.insert_one({"name": "Test Folder", "owner_id": "user123"})

    folders = await services.get_folders(owner_id="user456", session=session)

    assert not folders


@pytest.mark.asyncio
async def test__update_folder__given_valid_payload__should_return(session):
    result = await session.folders.insert_one(
        {"name": "Test Folder", "owner_id": "user123"}
    )

    payload = {"name": "Updated Folder"}
    await services.update_folder(
        owner_id="user123",
        folder_id=result.inserted_id,
        folder=payload,
        session=session,
    )

    updated_folder = await session.folders.find_one({"_id": result.inserted_id})

    assert updated_folder["name"] == payload["name"]


@pytest.mark.asyncio
async def test__delete_folder__given_existent_folder__should_delete(
    session,
):
    result = await session.folders.insert_one(
        {"name": "Test Folder", "owner_id": "user123"}
    )

    await services.delete_folder(
        owner_id="user123", folder_id=result.inserted_id, session=session
    )

    folder = await session.folders.find_one({"_id": result.inserted_id})

    assert not folder, "Folder was found"


@pytest.mark.asyncio
async def test__create_folder__given_existing_name__should_create_new(session):
    payload = {"name": "Test Folder"}
    await services.create_folder(owner_id="user123", folder=payload, session=session)

    duplicate_payload = {"name": "Test Folder"}
    await services.create_folder(
        owner_id="user123", folder=duplicate_payload, session=session
    )

    folders = await session.folders.find({"name": "Test Folder"}).to_list(None)

    assert len(folders) == 2


@pytest.mark.asyncio
async def test__get_folders__given_pagination__should_return_limited_results(session):
    folders = [
        {
            "name": f"Folder {i}",
            "created_at": f"2022-01-0{i}T00:00:00Z",
            "owner_id": "user123",
        }
        for i in range(5)
    ]
    await session.folders.insert_many(folders)

    retrieved_folders = await services.get_folders(
        owner_id="user123", session=session, limit=2, offset=1
    )

    assert len(retrieved_folders) == 2
    assert retrieved_folders[0]["name"] == "Folder 1"
    assert retrieved_folders[1]["name"] == "Folder 2"


@pytest.mark.asyncio
async def test__update_folder__given_non_existent_folder__should_not_fail(session):
    folder_id = str(ObjectId())
    payload = {"name": "Updated Folder"}

    await services.update_folder(
        owner_id="user123", folder_id=folder_id, folder=payload, session=session
    )

    folder = await session.folders.find_one({"_id": ObjectId(folder_id)})
    assert folder is None


@pytest.mark.asyncio
async def test__delete_folder__given_non_existent_folder__should_not_fail(session):
    folder_id = str(ObjectId())

    await services.delete_folder(
        owner_id="user123", folder_id=folder_id, session=session
    )

    folder = await session.folders.find_one({"_id": ObjectId(folder_id)})
    assert folder is None


@pytest.mark.asyncio
async def test__create_folder__should_log_event(session):
    payload = {"name": "Test Folder"}
    await services.create_folder(owner_id="user123", folder=payload, session=session)

    events = await session.events.find().to_list()

    assert len(events) == 1
    assert events[0]["type"] == FolderEventType.CREATED.value
    assert events[0]["payload"] == {**payload, "owner_id": "user123"}


@pytest.mark.asyncio
async def test__update_folder__should_log_event(session):
    result = await session.folders.insert_one(
        {"name": "Test Folder", "owner_id": "user123"}
    )

    await services.update_folder(
        owner_id="user123",
        folder_id=str(result.inserted_id),
        folder={"name": "Updated Folder"},
        session=session,
    )

    events = await session.events.find().to_list()

    assert len(events) == 1
    assert events[0]["type"] == FolderEventType.UPDATED.value
    assert events[0]["payload"] == {"name": "Updated Folder"}


@pytest.mark.asyncio
async def test__update_folder__given_no_user_folder__should_not_log_event(session):
    result = await session.folders.insert_one(
        {"name": "Test Folder", "owner_id": "user123"}
    )

    await services.update_folder(
        owner_id="user456",
        folder_id=str(result.inserted_id),
        folder={"name": "Updated Folder"},
        session=session,
    )

    events = await session.events.find().to_list()

    assert not events


@pytest.mark.asyncio
async def test__delete_folder__should_log_event(session):
    result = await session.folders.insert_one(
        {"name": "Test Folder", "owner_id": "user123"}
    )

    await services.delete_folder(
        owner_id="user123", folder_id=str(result.inserted_id), session=session
    )

    events = await session.events.find().to_list()

    assert len(events) == 1
    assert events[0]["type"] == FolderEventType.DELETED.value
    assert events[0]["payload"] == {}


@pytest.mark.asyncio
async def test__delete_folder__given_no_user_folder__should_not_log_event(session):
    result = await session.folders.insert_one(
        {"name": "Test Folder", "owner_id": "user123"}
    )

    await services.delete_folder(
        owner_id="user456", folder_id=str(result.inserted_id), session=session
    )

    events = await session.events.find().to_list()

    assert not events
