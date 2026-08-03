from typing import List

from fastapi import APIRouter, Query

from app.schemas.event_response import EventResponse
from app.services.event_service import event_service

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


@router.get(
    "/",
    response_model=List[EventResponse],
)
def get_events(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
):

    return event_service.get_events(page, size)