# Description
PythonコンテナでuWSGIとapp本体が動作するapサーバーです。

# Usage
## In Container
`uwsgi --http=0.0.0.0:5000 --wsgi-file=main.py --callable=app`
↓
`uwsgi --ini uwsgi.ini` でok。

※`python3 main.py`をすると`if __name__=='__main__'`が実行され、gunicornで動作してしまう。(多分)

## Out Container
`docker build ./ -t xxx-app`

`docker run -p 80:5000 -it xxx-app`

### 解説
`-p 80:5000`: PCのポート:コンテナのポート。こうすればPC側で`localhost:80`を開くとアプリが開く。

`-it`: コンソールに結果を出力。