from fastapi import WebSocketException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api.websocket_events import ServerEvent
from app.api.websocket_helpers import get_conversation_websocket_items
from app.api.websocket_manager import WebSocketManager


async def on_create_message(
    manager: WebSocketManager,
    current_user: models.User,
    db: Session,
    message_create: schemas.MessageCreate,
):
    message_conversation = crud.get_conversation(
        db=db, conversation_id=message_create.conversation_id
    )
    if message_conversation == None:
        raise WebSocketException(
            code=status.WS_1003_UNSUPPORTED_DATA,
            reason="The conversation must exist",
        )
    if current_user not in message_conversation.users:
        raise WebSocketException(
            code=status.WS_1003_UNSUPPORTED_DATA,
            reason="The current user must be in the conversation",
        )

    db_message = crud.create_message(db=db, message=message_create, author_id=current_user.id)

    await manager.emit(
        server_event_name=ServerEvent.NEW_MESSAGE,
        db_data=db_message,
        websocket_items=get_conversation_websocket_items(
            manager=manager,
            current_user=current_user,
            conversation_id=message_create.conversation_id,
        ),
        response_model=schemas.Message,
    )
