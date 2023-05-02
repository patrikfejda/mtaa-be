from enum import Enum


class ClientEvent(Enum):
    PING = "PING"
    CREATE_CONVERSATION = "CREATE_CONVERSATION"
    CREATE_MESSAGE = "CREATE_MESSAGE"


class ServerEvent(Enum):
    PONG = "PONG"
    NEW_CONVERSATION = "NEW_CONVERSATION"
    NEW_MESSAGE = "NEW_MESSAGE"
