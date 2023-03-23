from fastapi import APIRouter, Header, Request, Form, File, UploadFile
from typing import Annotated, List, Union, Optional
from typing import Union
from pydantic import BaseModel
from app.model.message import messageCreate, messageGet, messageConversationAll
from app.auth.verify import verify_token
from app.filestore.save import save_upload_file

router = APIRouter()

@router.post("/v1/message")
async def createMessage(
    conversation_id: int = Form(...),
    message: str = Form(...),
    photo: UploadFile = File(None),
    request: Request = None
):
    jwt = request.headers["Authorization"]
    id = request.headers["MyId"]
    verify_token(id, jwt)
    photo_url = save_upload_file(photo)
    message = messageCreate(sender_id=id, conversation_id=conversation_id, message=message, photo_url=photo_url)
    return {"detail": "ok", "message": message}