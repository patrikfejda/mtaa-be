from fastapi import APIRouter

from app.endpoints.v1 import (
    health,
    dbhealth,
    user,
    conversation,
)


router = APIRouter()
router.include_router(dbhealth.router)
router.include_router(health.router)
router.include_router(user.router)
router.include_router(conversation.router)

