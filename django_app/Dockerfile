FROM python:3.11.9-slim
LABEL authors="AlexeyInkov"

WORKDIR backend

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY db_device .

CMD ["gunicorn", "-b", "0.0.0.0:8000", "db_device.wsgi:application"]

