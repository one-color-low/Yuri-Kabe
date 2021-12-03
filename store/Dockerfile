FROM nginx:latest

# Nginx
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y vim locales
RUN apt-get install -y iputils-ping net-tools

# nginx.conf で include /etc/nginx/conf.d/*.conf; するので、好きな名前で設定ファイルを置けばOK。
COPY ./conf/store.conf /etc/nginx/conf.d/store.conf 

COPY ./sampleroom /var/www/sampleroom
COPY ./index.html /var/www/index.html
RUN chown -R www-data:www-data /var/www/sampleroom

CMD ["nginx", "-g", "daemon off;"]


# Python
RUN apt-get install -y python3-pip
RUN apt-get install -y libpcre3-dev
RUN apt-get install -y systemctl

RUN mkdir /uploader

COPY ./ /uploader

WORKDIR /uploader

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY ./conf/uwsgi.service /etc/systemd/system

CMD ["uwsgi","--ini","conf/uwsgi.ini"]

# dockerの制約でdeamon off。pythonとの順番変更必要？