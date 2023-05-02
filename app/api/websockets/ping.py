from sqlalchemy.orm import Session

from app import models, schemas
from app.api.websocket_events import ServerEvent
from app.api.websocket_manager import WebSocketItem, WebSocketManager


async def on_client_ping(
    manager: WebSocketManager,
    data: schemas.AppBaseModel,
    current_user: models.User,
    db: Session,
    websocket_item: WebSocketItem,
):
    await manager.emit(
        server_event_name=ServerEvent.PONG,
        db_data={},
        response_model=schemas.AppBaseModel,
        websocket_items={websocket_item},
    )
