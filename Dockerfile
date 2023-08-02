FROM python:3.9-alpine3.13
LABEL maintainer="zieft@hotmail.com"

ENV PYTHONUNBUFFERED 1 # Python 程序的输出将不会被缓冲，也就是说，输出会立即显示，而不是等到缓冲区满了或者正常退出时才显示。

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false # will be overrided by docker-compose.yml
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "ture" ]; \
        then /py/bin/pip install -r requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user