import csv
import os

from django.core.files.uploadedfile import InMemoryUploadedFile

from config import settings


def handle_uploaded_file(f: InMemoryUploadedFile):
    """Загрузка файла"""
    filename = os.path.join(settings.FILE_UPLOAD_DIR, f.name)
    with open(filename, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def check_csv_file(filename: str, fieldnames: list, encoding: str = "cp1251") -> bool:
    with open(filename, "r", encoding=encoding) as file:
        reader = csv.DictReader(file, delimiter=";")
        if reader.fieldnames != fieldnames:
            return False
        return True
