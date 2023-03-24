from fastapi import APIRouter

from app.endpoints.v1 import health, user, conversation, status, message


router = APIRouter()
router.include_router(health.router)
router.include_router(user.router)
router.include_router(conversation.router)
router.include_router(status.router)
router.include_router(message.router)
