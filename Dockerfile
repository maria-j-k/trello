FROM python:3
RUN apt-get update \
    && apt-get install -y postgresql-client \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY requirements.txt /code/

RUN /usr/local/bin/python -m pip install --upgrade pip
# RUN useradd -u 101 python
# USER python
RUN pip install -r requirements.txt
COPY . /code/
