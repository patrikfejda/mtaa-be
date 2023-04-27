from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.api.dependencies import CurrentWebsocketUserDependency, SessionDependency
from app.api.websocket import websocket_manager
from app.api.websocket_manager import WebSocketItem

router = APIRouter()

# TODO get all conversations endpoint


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
