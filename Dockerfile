FROM python:3
RUN apt-get update \
    && apt-get install -y postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN useradd -u 1000 -m python
USER python

ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY requirements.txt /code/

RUN pip install -r requirements.txt
COPY . /code/
