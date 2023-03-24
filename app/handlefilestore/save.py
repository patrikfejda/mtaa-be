import shutil
from pathlib import Path
import random, string
from fastapi import UploadFile
from app.config import FILESTORE_PATH, FILESTORE_URL


def generateFileName() -> str:
    return "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(40)
    )


def saveFilestore(uploadFile: UploadFile) -> None:
    if not uploadFile:
        return None
    suffix = Path(uploadFile.filename).suffix
    filename = generateFileName() + suffix

    destination = Path(f"{FILESTORE_PATH}/{filename}")
    url = f"{FILESTORE_URL}/{filename}"
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(uploadFile.file, buffer)
    finally:
        uploadFile.file.close()

    return url
