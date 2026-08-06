from fastapi import APIRouter
from app.services.metrics_service import metrics_service

router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"],
)

@router.get("/")
def get_metrics():
    return metrics_service.get_metrics()