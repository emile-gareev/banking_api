FROM python:3.9.13-slim-bullseye

COPY requirements*.txt /tmp/

RUN apt-get update && apt-get install -y --no-install-recommends vim iputils-ping \
net-tools netcat-traditional curl g++ unixodbc unixodbc-dev

RUN pip3 install -r /tmp/requirements.txt && pip3 install SQLAlchemy==1.4.44 --no-deps

WORKDIR /banking
ADD ./src ./
