from app.utils.timeout import timeout as utils_timeout


def create_websocket_message(token: str, event_name: str, data: dict):
    return {"token": token, "event": event_name, "data": data}


def websocket_receive_json_timeouted(websocket, timeout: int = 5):
    return utils_timeout(websocket.receive_json, timeout_duration=timeout)
