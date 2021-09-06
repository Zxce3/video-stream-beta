FROM python:latest

RUN apt-get update && apt-get upgrade -y
RUN apt-get install python3-pip -y
RUN apt-get install ffmpeg -y

COPY . /py
WORKDIR /py

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -U -r requirements.txt

CMD python3 -m bot
