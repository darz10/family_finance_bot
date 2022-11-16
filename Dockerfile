from python:3.9.6-buster

WORKDIR /app
COPY . .
RUN pip install --upgrade .