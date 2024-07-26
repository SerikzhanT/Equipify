FROM python:3.12-alpine3.20

COPY requirements.txt /temp/requirements.txt

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password eq_user

COPY backend /backend
WORKDIR /backend
EXPOSE 8000


USER eq_user



