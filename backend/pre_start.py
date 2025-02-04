import asyncio
import logging

import database

logger = logging.getLogger(__name__)


async def check_db_connection() -> None:
    status = await database.check_connection()
    logger.info(f"Database status: {status}")
    if not status.get("ok") == 1:
        raise Exception("Unable to connect to the Database")


if __name__ == "__main__":
    asyncio.run(check_db_connection())
