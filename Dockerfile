FROM python:3.11.9-slim
LABEL authors="AlexeyInkov"

WORKDIR backend

COPY requirements.txt .

RUN pip install - r requirements.txt

COPY django_app/db_device .



