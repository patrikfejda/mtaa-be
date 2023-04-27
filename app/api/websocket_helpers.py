from functools import reduce

from app import models

from .websocket_manager import WebSocketManager


def get_conversation_websocket_items(
    manager: WebSocketManager, current_user: models.User, conversation_id: int
):
    return reduce(
        lambda acc, item: acc.union({item})
        if item.has_conversation(conversation_id) and item.is_not_me(current_user.id)
        else acc,
        manager.active_websocket_items,
        set(),
    )


def get_users_websocket_items(
    manager: WebSocketManager, current_user: models.User, user_ids: set[int]
):
    return reduce(
        lambda acc, item: acc.union({item})
        if item.user_in(user_ids) and item.is_not_me(current_user.id)
        else acc,
        manager.active_websocket_items,
        set(),
    )
