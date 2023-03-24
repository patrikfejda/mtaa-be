from fastapi import APIRouter, Request, Form, File, UploadFile
from app.model.message import messageCreate, messageGet, messageConversationAll
from app.auth.verify import verifyToken
from app.handlefilestore.save import saveFilestore

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
    verifyToken(id, jwt)
    photoUrl = saveFilestore(photo)
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
    verifyToken(id, jwt)
    message = messageGet(userId=id, messageId=messageId)
    return {"detail": "ok", "message": message}


@router.get("/v1/message/all")
async def routerGetAllMessages(conversationId: int = Form(...), request: Request = None):
    jwt = request.headers["Authorization"]
    id = request.headers["MyId"]
    verifyToken(id, jwt)
    messages = messageConversationAll(userId=id, conversationId=conversationId)
    return {"detail": "ok", "messages": messages}
