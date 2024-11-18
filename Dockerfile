FROM python:3.11.9-slim
LABEL authors="AlexeyInkov"

RUN pip install --upgrade pip

COPY requirements.txt /temp/requirements.txt
RUN pip install -r /temp/requirements.txt

COPY db_device /db_device

WORKDIR db_device
EXPOSE 8000

RUN adduser --disabled-password service-user

USER service-user