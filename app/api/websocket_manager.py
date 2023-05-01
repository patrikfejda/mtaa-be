import json
from typing import Any, Callable, Coroutine

from fastapi import WebSocket, WebSocketDisconnect, WebSocketException, status
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth.helpers import get_user_by_token_or_fail
from app.utils.parameter import get_pydantic_parameter_type
from app.utils.websocket import websocket_message_receive_json_or_throw

from .websocket_events import ServerEvent

EventFunc = Callable[["WebSocketManager", Session, schemas.AppBaseModel], Coroutine]


class WebSocketItem:
    def __init__(self, user_id: int, websocket: WebSocket, conversation_ids: set[int] = []):
        self._user_id = user_id
        self._websocket = websocket
        self._conversation_ids = set(conversation_ids)

    def user_in(self, ids: set[int]):
        return self._user_id in ids

    def has_conversation(self, id: int):
        return id in self._conversation_ids

    def add_conversation(self, id: int):
        self._conversation_ids.add(id)

    def get_connection(self):
        return self._websocket


class WebSocketManager:
    def __init__(self):
        self.active_websocket_items: list[WebSocketItem] = []
        self.client_events: dict[str, tuple[EventFunc, schemas.AppBaseModel]] = {}

    async def connect(self, current_user: models.User, db: Session, websocket_item: WebSocketItem):
        connection = websocket_item.get_connection()

        await connection.accept()
        self.active_websocket_items.append(websocket_item)

        try:
            while True:
                websocket_message = schemas.WebSocketMessageClient.parse_obj(
                    await websocket_message_receive_json_or_throw(connection)
                )

                await self.auth_handler(db=db, websocket_message=websocket_message)
                await self.event_handler(
                    current_user=current_user, db=db, websocket_message=websocket_message
                )

        except WebSocketDisconnect:
            self.disconnect(websocket_item)
            await connection.close()
        except ValidationError:
            self.disconnect(websocket_item)
            raise WebSocketException(
                code=status.WS_1003_UNSUPPORTED_DATA,
                reason="Could not validate the websocket message",
            )
        except WebSocketException as exception:
            self.disconnect(websocket_item)
            raise exception

    def disconnect(self, websocket_item: WebSocketItem):
        if websocket_item in self.active_websocket_items:
            self.active_websocket_items.remove(websocket_item)

    async def auth_handler(self, db: Session, websocket_message: schemas.WebSocketMessageClient):
        ws_credentials_exception = WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION, reason="Could not validate credentials"
        )
        return await get_user_by_token_or_fail(
            db=db, token=websocket_message.token, exception=ws_credentials_exception
        )

    async def event_handler(
        self,
        current_user: models.User,
        db: Session,
        websocket_message: schemas.WebSocketMessageClient,
    ):
        func, schema = self.client_events[websocket_message.event]
        await func(self, current_user, db, schema(**websocket_message.data))

    async def emit(
        self,
        server_event_name: ServerEvent,
        db_data: Any,
        response_model: schemas.AppBaseModel,
        websocket_items: set[WebSocketItem],
        websocket_item_side_effect: Callable[[WebSocketItem], None] = None,
    ):
        for item in websocket_items:
            if websocket_item_side_effect:
                websocket_item_side_effect(item)

            await item.get_connection().send_json(
                json.loads(
                    schemas.WebSocketMessageServer(
                        event=server_event_name, data=response_model.from_orm(db_data)
                    ).json(by_alias=True)
                )
            )

    def register_event(self, event_name: str, func: EventFunc):
        schema = get_pydantic_parameter_type(func)
        self.client_events[event_name] = (func, schema)
