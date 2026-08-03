from fastapi import APIRouter

from app.services.event_service import event_service

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

@router.get("/")
def get_events():

    return event_service.get_events()