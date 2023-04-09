from fastapi import APIRouter, File, Form, Request, UploadFile

from app.models.__old__message import messageConversationAll, messageCreate, messageGet
from app.utils.filestore import save_to_filestore

router = APIRouter()


@router.post("/v1/message")
async def routerCreateMessage(
    conversationId: int = Form(...),
    message: str = Form(...),
    photo: UploadFile = File(None),
    request: Request = None,
):
    jwt = request.headers["Authorization"]
    id = request.headers["MyId"]

    photoUrl = save_to_filestore(photo)
    message = messageCreate(
        senderId=id,
        conversationId=conversationId,
        message=message,
        photoUrl=photoUrl,
    )
    return {"detail": "ok", "message": message}


@router.get("/v1/message")
async def routerGetMessage(messageId: int = Form(...), request: Request = None):
    jwt = request.headers["Authorization"]
    id = request.headers["MyId"]

    message = messageGet(userId=id, messageId=messageId)
    return {"detail": "ok", "message": message}


@router.get("/v1/message/all")
async def routerGetAllMessages(conversationId: int = Form(...), request: Request = None):
    jwt = request.headers["Authorization"]
    id = request.headers["MyId"]

    messages = messageConversationAll(userId=id, conversationId=conversationId)
    return {"detail": "ok", "messages": messages}
