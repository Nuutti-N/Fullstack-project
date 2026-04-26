
from backend.models import HealthCheck
from fastapi import APIRouter, status

router = APIRouter()


@router.get("/health", tags=["healthcheck"], summary="Perform a healthcheck",
            response_description="Return HTTP status code 200 (OK)", status_code=status.HTTP_200_OK, response_model=HealthCheck)
def get_health() -> HealthCheck:
    return HealthCheck(status="OK")
