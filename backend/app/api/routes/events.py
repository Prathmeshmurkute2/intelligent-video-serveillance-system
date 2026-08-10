from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.exceptions.event import EventNotFoundException
from app.schemas.api_response import ApiResponse
from app.services.event_service import event_service


router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


@router.get("/test-error")
def test():

    raise EventNotFoundException()


@router.get("/")
def get_events(
    page: int = 1,
    size: int = 20,
    db: Annotated[Session, Depends(get_db)] = None,
):

    events = event_service.get_events(
        db=db,
        page=page,
        size=size,
    )

    return ApiResponse(
        message="Events retrieved successfully.",
        data=events,
    )