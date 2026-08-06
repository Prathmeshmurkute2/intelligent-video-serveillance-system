from fastapi import APIRouter

from app.services.health_service import health_service

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("/")
def get_health():
    return health_service.get_health()