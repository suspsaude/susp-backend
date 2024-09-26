FROM python:3.12-slim-bookworm

WORKDIR /app

RUN apt update && apt install -y \
    curl

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .
