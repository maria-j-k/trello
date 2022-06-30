FROM python:3
RUN apt-get update && apt-get install -y build-essential python3-dev libldap2-dev libsasl2-dev

RUN mkdir /code

RUN pip3 install pip==21.2.3
COPY requirements.txt /code/
RUN pip3 install -r /code/requirements.txt

WORKDIR /code
COPY . /code/
