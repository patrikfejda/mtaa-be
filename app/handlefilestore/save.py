import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Callable
import random, string
from fastapi import UploadFile
from app.config import FILESTORE_PATH, FILESTORE_URL

def generateFileName() -> str:
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(40))

def save_upload_file(upload_file: UploadFile) -> None:
    if not upload_file:
        return None
    suffix = Path(upload_file.filename).suffix
    filename = generateFileName() + suffix

    destination = Path(f"{FILESTORE_PATH}/{filename}")
    url = f"{FILESTORE_URL}/{filename}"
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()
    
    return url
