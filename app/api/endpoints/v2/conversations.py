from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app import schemas
from app.api.dependencies import (
    CurrentUserDependency,
    CurrentWebsocketUserDependency,
    SessionDependency,
)
from app.api.websocket import websocket_manager
from app.api.websocket_manager import WebSocketItem

router = APIRouter()


@router.get("/", response_model=list[schemas.Conversation])
def get_all_user_conversation(current_user: CurrentUserDependency, db: SessionDependency):
    return current_user.conversations


@router.websocket("/ws")
async def create_conversations_websocket(
    websocket: WebSocket, current_user: CurrentWebsocketUserDependency, db: SessionDependency
):
    websocket_item = WebSocketItem(
        user_id=current_user.id,
        websocket=websocket,
        conversation_ids=set(map(lambda conversation: conversation.id, current_user.conversations)),
    )
    await websocket_manager.connect(current_user=current_user, db=db, websocket_item=websocket_item)
