from datetime import datetime

from fastapi import APIRouter

from app.websocket.publisher import event_publisher


router = APIRouter(
    prefix="/demo",
    tags=["Demo"],
)


@router.post("/event")
async def send_demo_event():

    await event_publisher.publish_event(
        "event_created",
        {
            "event_type": "line_crossing",
            "camera_id": "Gate-1",
            "track_id": 1,
            "severity": "INFO",
            "message": "Person crossed gate",
            "timestamp": datetime.now().isoformat(),
            "metadata": {
                "direction": "IN",
            },
        },
    )

    return {
        "success": True,
        "message": "Demo event broadcast successfully.",
    }