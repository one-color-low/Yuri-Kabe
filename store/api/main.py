from flask import Flask, request, jsonify
import zipfile, os
import database
from models.models import *

import random
import uuid

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

        room_id = str(uuid.uuid1())
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

        return jsonify([room_id, request.form['title'], request.form['description']])

    else:

        return "ng"


# jsonでroom_infoテーブルを上から10個返すAPI
@app.route('/get_list', methods=['GET', 'POST'])
def get_list():
    table = RoomOperation.get_latest_n(1)
    data_list = []
    for row in table:
        data = [row.id, row.title, row.description]
        data_list.append(data)
    return jsonify(data_list)


if __name__ == "__main__":
    app.run()

