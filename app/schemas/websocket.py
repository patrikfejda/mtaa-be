from app.api.websocket_events import ClientEvent, ServerEvent
from app.schemas.base_model import AppBaseModel


class WebSocketMessageClient(AppBaseModel):
    token: str
    event: ClientEvent
    data: dict


class WebSocketMessageServer(AppBaseModel):
    event: ServerEvent
    data: AppBaseModel
