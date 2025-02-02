from typing import TYPE_CHECKING

import pytest
from database import get_client
from httpx import ASGITransport, AsyncClient
from main import app
from pytest_asyncio import is_async_test

if TYPE_CHECKING:
    from typing import AsyncGenerator

    from database import Session


def pytest_collection_modifyitems(items):
    # https://pytest-asyncio.readthedocs.io/en/v0.24.0/how-to-guides/run_session_tests_in_same_loop.html
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(loop_scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


# TODO: Improve. We should not need to drop all collections after each test, just the objects created by the test.
@pytest.fixture(autouse=True)
async def cleanup(session: "Session"):
    db = session.client.db
    async with session.start_transaction():
        for collection in await db.list_collection_names():
            await db[collection].delete_many({}, session=session)


@pytest.fixture
async def session() -> "AsyncGenerator[Session, None]":
    async with await get_client().start_session() as session:
        yield session


@pytest.fixture
async def client() -> "AsyncGenerator[AsyncClient, None]":
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
