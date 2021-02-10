FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y postgresql-client git libjpeg-dev zlib1g-dev gcc libc-dev libpq-dev libblas-dev libfreetype6-dev

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD []
