import os

from django.core.files.uploadedfile import InMemoryUploadedFile

from config import settings


def handle_uploaded_file(f: InMemoryUploadedFile):
    filename = os.path.join(settings.FILE_UPLOAD_DIR, f.name)
    with open(filename, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
