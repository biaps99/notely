import asyncio
import logging

import database
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

logger = logging.getLogger(__name__)

stop_after_seconds = 5
wait_seconds = 1


@retry(
    stop=stop_after_attempt(stop_after_seconds),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.INFO),
)
async def check_db_connection() -> None:
    return await database.check_connection()


if __name__ == "__main__":
    asyncio.run(check_db_connection())
