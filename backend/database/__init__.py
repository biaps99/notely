from typing import TYPE_CHECKING

from motor import motor_asyncio
from pymongo.driver_info import DriverInfo

from __version__ import __version__
from settings import settings

if TYPE_CHECKING:
    from typing import AsyncGenerator, Optional

    from motor.core import TransactionOptions


class Session(motor_asyncio.AsyncIOMotorClientSession):
    events: "motor_asyncio.AsyncIOMotorCollection"
    notes: "motor_asyncio.AsyncIOMotorCollection"
    folders: "motor_asyncio.AsyncIOMotorCollection"


class Client(motor_asyncio.AsyncIOMotorClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = self.get_database()

    async def start_session(
        self,
        causal_consistency: "Optional[bool]" = None,
        default_transaction_options: "Optional[TransactionOptions]" = None,
        snapshot: "Optional[bool]" = False,
    ) -> "Session":
        session = await super().start_session(
            causal_consistency, default_transaction_options, snapshot
        )
        await self._add_collection_attrs_to_session(session)
        return session

    async def _add_collection_attrs_to_session(self, session: "Session"):
        """Since all Collections are in a single Database,
        dynamically add attributes to each Session object for each Collection.

        Instead of doing `session.client.database_name.collection_name`,
        do `session.collection_name` for simplicity."""
        session.events = self.db.events
        session.notes = self.db.notes
        session.folders = self.db.folders


client = Client(
    host=settings.MONGODB_CONNECTION_STRING,
    driver=DriverInfo(name=settings.ROOT_DIR_NAME, version=__version__),
    tz_aware=True,
)


async def get_session() -> "AsyncGenerator[Session, None]":
    async with await client.start_session() as session:
        yield session


async def check_connection():
    return await client.db.command("ping")


async def close_connection():
    client.close()


def get_client() -> Client:
    return client


__all__ = ["get_client", "get_session", "check_connection", "close_connection"]
