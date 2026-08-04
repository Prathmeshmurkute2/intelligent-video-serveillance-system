from fastapi import APIRouter

from app.services.dashboard_service import dashboard_service
from app.schemas.api_response import ApiResponse


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)

@router.get("/")
def get_dashboard():

    dashboard = dashboard_service.get_dashboard()

    return ApiResponse(
        message="Dashboard retrieved successfully.",
        data=dashboard,
    )