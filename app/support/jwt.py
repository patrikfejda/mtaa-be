from uuid import uuid4


def generate_jwt() -> str:
    return uuid4()
