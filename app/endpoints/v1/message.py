from fastapi import APIRouter, Header, Request, Form, File, UploadFile
from typing import Annotated, List, Union, Optional
from typing import Union
from pydantic import BaseModel
from app.model.message import messageCreate, messageGet, messageConversationAll
from app.auth.verify import verify_token
from app.handlefilestore.save import save_upload_file

router = APIRouter()


@router.post("/v1/message")
async def createMessage(
    conversationId: int = Form(...),
    message: str = Form(...),
    photo: UploadFile = File(None),
    request: Request = None,
):
    jwt = request.headers["Authorization"]
    id = request.headers["MyId"]
    verify_token(id, jwt)
    photoUrl = save_upload_file(photo)
    message = messageCreate(
        senderId=id,
        conversationId=conversationId,
        message=message,
        photoUrl=photoUrl,
    )
    return {"detail": "ok", "message": message}


@router.get("/v1/message")
async def getMessage(messageId: int = Form(...), request: Request = None):
    jwt = request.headers["Authorization"]
    id = request.headers["MyId"]
    verify_token(id, jwt)
    message = messageGet(userId=id, messageId=messageId)
    return {"detail": "ok", "message": message}

@router.get("/v1/message/all")
async def getAllMessages(conversationId: int = Form(...), request: Request = None):
    jwt = request.headers["Authorization"]
    id = request.headers["MyId"]
    verify_token(id, jwt)
    messages = messageConversationAll(userId=id, conversationId=conversationId)
    return {"detail": "ok", "messages": messages}