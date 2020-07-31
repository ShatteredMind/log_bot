FROM python:3.7

WORKDIR /app
COPY . /app

ENV PATH=$PATH:/app
ENV PYTHONPATH /app
ENV PYTHONUNBUFFERED=1

RUN pip install --disable-pip-version-check -r requirements.txt
