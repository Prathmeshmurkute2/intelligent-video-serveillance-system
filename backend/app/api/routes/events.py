from typing import List

from fastapi import APIRouter, Query

from app.schemas.event_response import EventResponse
from app.services.event_service import event_service
from app.exceptions.event import EventNotFoundException
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db

from typing import Annotated

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

@router.get("/test-error")
def test():

    raise EventNotFoundException()


@router.get("/")
def get_events(
    page: int = 1,
    size: int = 20,
    db: Annotated[Session, Depends(get_db)]=None,
):

    return event_service.get_events(db=db,
                                    page=page,
                                     size= size)