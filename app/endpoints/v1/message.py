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
    photo_url = save_upload_file(photo)
    message = messageCreate(
        sender_id=id,
        conversationId=conversationId,
        message=message,
        photo_url=photo_url,
    )
    return {"detail": "ok", "message": message}


@router.get("/v1/message")
async def getMessage(messageId: int = Form(...), request: Request = None):
    jwt = request.headers["Authorization"]
    id = request.headers["MyId"]
    verify_token(id, jwt)
    message = messageGet(user_id=id, messageId=messageId)
    return {"detail": "ok", "message": message}

@router.get("/v1/message/all")
async def getAllMessages(conversationId: int = Form(...), request: Request = None):
    jwt = request.headers["Authorization"]
    id = request.headers["MyId"]
    verify_token(id, jwt)
    messages = messageConversationAll(user_id=id, conversationId=conversationId)
    return {"detail": "ok", "messages": messages}