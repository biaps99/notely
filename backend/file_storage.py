import os
import aiofiles
from fastapi import File
from settings import settings
from importlib import import_module


def import_string(dotted_path: str):
    module_path, _, attr = dotted_path.rpartition(".")
    module = import_module(module_path)
    return getattr(module, attr)


async def upload_to_fs(owner_id: str, _file: File, location: str) -> str:
    file_location = f"{location}/{owner_id}/{_file.filename}"
    os.makedirs(os.path.dirname(file_location), exist_ok=True)

    async with aiofiles.open(file_location, "wb") as buffer:
        while chunk := await _file.read(1024):
            await buffer.write(chunk)

    return file_location


async def upload_to_tmp(owner_id: str, _file: File, location: str) -> str:
    return f"{location}/{owner_id}/{_file.filename}"


async def upload(
    owner_id: str, _file: File, location: str = settings.UPLOAD_DIR_NAME
) -> str:
    file_storage_upload_func = import_string(settings.FILE_STORAGE_UPLOAD_PATH)
    file_path = await file_storage_upload_func(owner_id, _file, location)
    return f"{settings.UPLOAD_URL}/{file_path}"


__all__ = ["upload"]
