import csv
import os

import chardet
from chardet.enums import LanguageFilter
from chardet.universaldetector import UniversalDetector
from django.core.files.uploadedfile import InMemoryUploadedFile

from config import settings


def handle_uploaded_file(f: InMemoryUploadedFile) -> None:
    """Загрузка файла"""
    filename = os.path.join(settings.FILE_UPLOAD_DIR, f.name)
    with open(filename, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def get_file_encoding(file_path: str) -> str:
    """Получение кодировки файла"""
    with open(file_path, "rb") as f:
        detector = UniversalDetector()
        detector.reset()
        for line in f.readlines():
            detector.feed(line)
        detector.close()
        result = detector.result["encoding"]
        if result == "windows-1251":
            return "cp1251"
        return result


def check_csv_file(file_path: str, fieldnames: list, encoding: str) -> bool:
    """Проверка заголовков таблицы csv файла"""
    with open(file_path, "r", encoding=encoding) as file:
        reader = csv.DictReader(file, delimiter=";")
        if reader.fieldnames != fieldnames:
            return False
        return True
