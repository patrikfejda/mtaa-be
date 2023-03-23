import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Callable
import random, string
from fastapi import UploadFile


def save_upload_file(upload_file: UploadFile) -> None:
    suffix = Path(upload_file.filename).suffix
    destination_str = "/public/images/" + "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(40)
    ) + suffix

    destination = Path(destination_str)
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()
    
    return destination_str
