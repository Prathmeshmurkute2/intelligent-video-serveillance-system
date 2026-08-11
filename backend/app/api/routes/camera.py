import asyncio

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.services.video_service import video_service


router = APIRouter(
    prefix="/camera",
    tags=["Camera"],
)


@router.get("/stream")
async def stream_camera():

    loop = asyncio.get_running_loop()

    return StreamingResponse(
        video_service.generate_frames(
            event_loop=loop
        ),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )