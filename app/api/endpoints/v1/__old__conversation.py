from fastapi import APIRouter, Form, Request

from app.models.__old__conversation import (
    conversationCreate,
    conversationGet,
    conversationsGetAll,
    verifyUserInConversation,
)

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

    conversations = conversationsGetAll(id)

    return {"detail": "ok", "conversations": conversations}
