from fastapi import APIRouter, Request, Form
from app.model.conversation import (
    conversationCreate,
    conversationGet,
    verifyUserInConversation,
    conversationsGetAll,
)
from app.auth.verify import verifyToken

router = APIRouter()


@router.post("/v1/conversation")
async def routerCreateConversation(
    name: str = Form(...),
    userIds: list = Form(...),
    isGroup: bool = Form(...),
    request: Request = None,
):
    jwt = request.headers["Authorization"]
    id = request.headers["MyId"]
    verifyToken(id, jwt)
    if not id in userIds:
        userIds.append(id)
    conversation = conversationCreate(name, userIds, isGroup)

    return {
        "detail": "ok",
        "conversation": conversation,
    }


@router.get("/v1/conversation")
async def routerGetConversation(
    conversationId: int = Form(...),
    request: Request = None,
):
    jwt = request.headers["Authorization"]
    id = request.headers["MyId"]
    verifyToken(id, jwt)
    verifyUserInConversation(id, conversationId)
    conversation = conversationGet(conversationId)

    return {
        "detail": "ok",
        "conversation": conversation,
    }


@router.get("/v1/conversation/all")
async def routerGetAllConversations(
    request: Request = None,
):
    jwt = request.headers["Authorization"]
    id = request.headers["MyId"]
    verifyToken(id, jwt)

    conversations = conversationsGetAll(id)

    return {"detail": "ok", "conversations": conversations}
