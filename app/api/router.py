from fastapi import APIRouter

from .endpoints.v2 import auth, statuses, users

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(statuses.router, prefix="/statuses", tags=["statuses"])
