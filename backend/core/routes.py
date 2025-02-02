from typing import TYPE_CHECKING

from core import constants, schemas, services
from database import get_session
from fastapi import APIRouter, Depends

if TYPE_CHECKING:
    from database import Session

router = APIRouter(prefix=constants.API_PREFIX)


@router.get("/events", response_model=list[schemas.EventRetrieve])
async def get_events(
    session: "Session" = Depends(get_session),
) -> list["schemas.EventRetrieve"]:
    return await services.get_events(session)
