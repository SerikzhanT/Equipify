FROM python:3.12-alpine3.20

COPY requirements.txt /temp/requirements.txt

COPY backend /backend

WORKDIR /backend

EXPOSE 8000

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password eq_user

USER eq_user
