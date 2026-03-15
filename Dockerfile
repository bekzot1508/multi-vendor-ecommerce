FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements/base.txt /tmp/requirements-base.txt
RUN pip install --upgrade pip && pip install -r /tmp/requirements-base.txt

COPY . /app