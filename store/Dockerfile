FROM nginx:latest

# Nginx
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y vim locales
RUN apt-get install -y iputils-ping net-tools sqlite3

## nginx.conf で include /etc/nginx/conf.d/*.conf; するので、好きな名前で設定ファイルを置けばOK。
COPY ./conf/store.conf /etc/nginx/conf.d/store.conf
RUN mkdir /var/log/uwsgi

# Python
RUN apt-get install -y python3-pip
RUN apt-get install -y libpcre3-dev
RUN apt-get install -y systemctl

COPY ./api /api

WORKDIR /api

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY ./api/uwsgi/uwsgi.service /etc/systemd/system


#RUN uwsgi --ini conf/uwsgi.ini

# 以下CMD(コンテナ起動時に実行されるコマンド)

## nginxを起動(deamon offは必須)
#CMD ["nginx", "-g", "daemon off;"]

## デーモンとしてuwsgiを起動
#CMD ["uwsgi","--ini","conf/uwsgi.ini"]

# 多分上のCMDがフォアグラウンドで実行されて(pid 1)、下のCMDが実行されない。
# Nginxはどっちにしろ起動されるっぽいので、uwsgi実行コマンドをいい感じにできるといいね。(最悪手動でもいいけど)