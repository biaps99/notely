from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends

from core import auth, constants, schemas, services
from database import get_session

if TYPE_CHECKING:
    from database import Session

router = APIRouter(prefix=constants.API_PREFIX)


@router.get("/events", response_model=list[schemas.EventRetrieve])
async def get_events(
    session: "Session" = Depends(get_session),
    auth_user: dict = Depends(auth.get_auth_user),
) -> list["schemas.EventRetrieve"]:
    return await services.get_events(session)
