from fastapi import APIRouter

from app.schemas.api_response import ApiResponse

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

@router.get("/healthy")
def healthy():
    return ApiResponse(
        message="Service is healthy.",
        data={
            "status": "healthy",
            "version": "1.0.0"
        }
    )