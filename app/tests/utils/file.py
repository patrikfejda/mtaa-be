from os import path

from app.config import ROOT_DIR


def get_file_and_extension(filename: str):
    file_path = path.join(ROOT_DIR, "static", filename)
    _, file_extension = path.splitext(file_path)
    file = open(file_path, "rb")
    return file, file_extension
