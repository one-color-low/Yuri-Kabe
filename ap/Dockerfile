FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install -y python3-pip
RUN apt-get install -y libpcre3-dev
RUN apt-get install -y systemctl
RUN apt-get install -y vim
RUN apt-get install -y iputils-ping net-tools

RUN mkdir /Yuri-Kabe

COPY ./ /Yuri-Kabe

WORKDIR /Yuri-Kabe

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY ./uwsgi.service /etc/systemd/system

CMD ["uwsgi","--ini","uwsgi.ini"]