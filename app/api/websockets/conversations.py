from fastapi import WebSocketException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api.websocket_events import ServerEvent
from app.api.websocket_helpers import get_users_websocket_items
from app.api.websocket_manager import WebSocketManager


async def on_create_conversation(
    manager: WebSocketManager,
    current_user: models.User,
    db: Session,
    conversation_create: schemas.ConversationCreate,
):
    if not conversation_create.is_group and len(conversation_create.user_ids) != 2:
        raise WebSocketException(
            code=status.WS_1003_UNSUPPORTED_DATA, reason="Direct conversation must have two users"
        )
    if conversation_create.is_group and len(conversation_create.user_ids) < 2:
        raise WebSocketException(
            code=status.WS_1003_UNSUPPORTED_DATA,
            reason="Group conversation must have at least two users",
        )
    if conversation_create.is_group and not conversation_create.name:
        raise WebSocketException(
            code=status.WS_1003_UNSUPPORTED_DATA,
            reason="Group conversation must have a name",
        )
    if current_user.id not in conversation_create.user_ids:
        raise WebSocketException(
            code=status.WS_1003_UNSUPPORTED_DATA,
            reason="The conversation must have the current user in user_ids",
        )
    if not conversation_create.is_group:
        other_user_id = next(filter(lambda id: id != current_user.id, conversation_create.user_ids))
        other_user = crud.get_user(db=db, user_id=other_user_id)

        if (
            db.query(models.Conversation)
            .filter(
                models.Conversation.is_group.is_(False),
                models.Conversation.users.any(models.User.id == current_user.id),
                models.Conversation.users.any(models.User.id == other_user_id),
            )
            .first()
        ):
            raise WebSocketException(
                code=status.WS_1003_UNSUPPORTED_DATA,
                reason="Direct conversation with this user already exists",
            )

        conversation_create.name = other_user.display_name or other_user.username

    db_conversation = crud.create_conversation(
        db=db, conversation=conversation_create, author_id=current_user.id
    )
    await manager.emit(
        server_event_name=ServerEvent.NEW_CONVERSATION,
        db_data=db_conversation,
        websocket_items=get_users_websocket_items(
            manager=manager, current_user=current_user, user_ids=conversation_create.user_ids
        ),
        websocket_item_side_effect=lambda item: item.add_conversation(db_conversation.id),
        response_model=schemas.Conversation,
    )
