from fastapi import WebSocket, WebSocketException, status


async def websocket_message_receive_json_or_throw(websocket: WebSocket):
    try:
        message = await websocket.receive_json()
        return message
    except Exception:
        WebSocketException(
            code=status.WS_1003_UNSUPPORTED_DATA,
            reason="You can only send serialized JSON messages",
        )
