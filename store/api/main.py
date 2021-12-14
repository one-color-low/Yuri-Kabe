from flask import Flask, request, jsonify
import zipfile, os
import database
from models.models import *

import random

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "/var/www"

db_uri = "sqlite:///" + os.path.join(app.root_path, 'oshikabe.db')
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# DB init
database.init_db(app)

#Roomアップロード用API
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':

        room_id = str(random.uniform(100, 200)) #todo: DBを参照して連続値を入れるように
        author = "anonymous"

        #ファイル保存
        file = request.files['zip_input']
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], room_id)

        with zipfile.ZipFile(file) as existing_zip:
            existing_zip.extractall(path=upload_path)

        #DB更新
        RoomOperation.add_entry(
            id=room_id,
            author=author,
            title=request.form['title'],
            description=request.form['description']
        )

        room_url = "http://localhost/store/" + room_id + "/1st/" #最後の"/"が無いと勝手にリダイレクトされるので注意

        return jsonify([room_url, room_id])

    else:

        return "ng"


# jsonでroom_infoテーブルを上から10個返すAPI
@app.route('/get_list', methods=['GET', 'POST'])
def get_list():
    table = RoomOperation.get_latest_n(1)
    id_list = []
    title_list = []
    description_list = []
    for row in table:
        id_list.append(row.id)
        title_list.append(row.title)
        description_list.append(row.description)
    return jsonify([id_list, title_list, description_list])
    #return "ok"


if __name__ == "__main__":
    app.run()

