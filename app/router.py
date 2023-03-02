from fastapi import APIRouter

from app.endpoints.v1 import (
    health,
    dbhealth,
)

router = APIRouter()
router.include_router(dbhealth.router)
router.include_router(health.router)