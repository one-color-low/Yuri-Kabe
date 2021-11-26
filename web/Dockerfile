FROM nginx:latest

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y vim locales

# デフォルトの設定があるから、わざわざ用意しなくてOK。
#COPY ./nginx.conf /etc/nginx/nginx.conf 

# nginx.conf で include /etc/nginx/conf.d/*.conf; するので、好きな名前で設定ファイルを置けばOK。
COPY ./conf/uwsgi.conf /etc/nginx/conf.d/uwsig.conf 

CMD ["nginx", "-g", "daemon off;"]