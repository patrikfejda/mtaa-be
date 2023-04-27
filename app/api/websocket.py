from app.api.websockets.conversations import on_create_conversation
from app.api.websockets.messages import on_create_message

from .websocket_events import ClientEvent
from .websocket_manager import WebSocketManager

websocket_manager = WebSocketManager()
websocket_manager.register_event(ClientEvent.CREATE_CONVERSATION, on_create_conversation)
websocket_manager.register_event(ClientEvent.CREATE_MESSAGE, on_create_message)
