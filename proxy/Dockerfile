FROM python:3.10-alpine3.13
LABEL maintainer="chriskondracki"

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app

RUN apk add --no-cache \
        git \
        build-base && \
    python -m venv /py && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        flaskuser

USER flaskuser