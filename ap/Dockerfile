FROM ubuntu

RUN apt-get update -y
RUN apt-get install -y python3-pip
RUN apt-get install -y libpcre3-dev

COPY ./ /Yuri-Kabe

WORKDIR /Yuri-Kabe

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD ["uwsgi","--ini","uwsgi.ini"]