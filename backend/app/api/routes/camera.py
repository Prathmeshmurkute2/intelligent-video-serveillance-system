from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.services.video_service import video_service


router = APIRouter(
    prefix="/camera",
    tags=["Camera"],
)


@router.get("/stream")
def stream_camera():

    return StreamingResponse(
        video_service.generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )