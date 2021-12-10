FROM nginx:latest

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y vim locales
RUN apt-get install -y iputils-ping net-tools

# nginx.conf で include /etc/nginx/conf.d/*.conf; するので、好きな名前で設定ファイルを置けばOK。
COPY ./conf/web.conf /etc/nginx/conf.d/web.conf 

# トップページの設定
COPY ./static /var/www
RUN chown -R www-data:www-data /var/www

# デフォルトのパーミッション設定
WORKDIR /var/www
RUN umask 000

CMD ["nginx", "-g", "daemon off;"]