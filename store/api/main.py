from flask import Flask, request, jsonify, flash, redirect
import zipfile, os
import database
from models.models import *
import requests, json

import random
import uuid

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "/var/www"

db_uri = "sqlite:///" + os.path.join(app.root_path, 'oshikabe.db')
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# DB init
database.init_db(app)

@app.route('/register', methods=['POST'])
def register():

    # user_name
    if 'user_name' not in request.form:
        return jsonify({'message': 'No user_name part.'}), 400

    user_name = request.form['user_name']

    if user_name == '':
        return jsonify({'message': 'No input user_name.'}), 400

    # id_token -> google_subの取得
    if 'id_token' not in request.form:
        return jsonify({'message': 'No id_token part.'}), 400

    id_token = request.form['id_token']

    if id_token == '':
        return jsonify({'message': 'No input id_token.'}), 400

    params = (
        ('id_token', str(id_token) ),
    )

    response = requests.get('https://oauth2.googleapis.com/tokeninfo', params=params)
    
    response_dict = json.loads(response.text)

    google_sub = response_dict["sub"]

    # user_idの生成
    user_id = str(uuid.uuid1())

    # tokenをDBに保存
    UserOperation.add_entry(
        id=user_id,
        name=user_name,
        google_sub=google_sub
    )

    return "ok"

#Roomアップロード用API
@app.route('/upload', methods=['GET', 'POST'])
def upload():

    if request.method != 'POST':
        return jsonify({'message': 'Unexpected request type.'}), 400

    if 'zip_input' not in request.files:
        return jsonify({'message': 'No file part.'}), 400

    file = request.files['zip_input'] 

    if file.filename == '':
        return jsonify({'message': 'No selected file.'}), 400
    

    if 'title' not in request.form:
        return jsonify({'message': 'No title part.'}), 400

    title = request.form['title']

    if title == '':
        return jsonify({'message': 'No input title.'}), 400


    if 'description' not in request.form:
        return jsonify({'message': 'No description part.'}), 400

    description = request.form['description']

    if description == '':
        return jsonify({'message': 'No input description.'}), 400
    

    if 'id_token' not in request.form:
        return jsonify({'message': 'No id_token part.'}), 400

    id_token = request.form['id_token']

    if id_token == '':
        return jsonify({'message': 'No input id_token.'}), 400

    params = (
        ('id_token', str(id_token) ),
    )

    response = requests.get('https://oauth2.googleapis.com/tokeninfo', params=params)
    
    response_dict = json.loads(response.text)

    google_sub = response_dict["sub"]

    # google_subをもとに、Userテーブルからauthorのuser_idを取得
    author = UserOperation.get_id_from_google_sub(google_sub)

    if author == "not found":
        return jsonify({'message': 'Unvalid User.'}), 400

    room_id = str(uuid.uuid1())

    #ファイル保存
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], room_id)
    with zipfile.ZipFile(file) as existing_zip:
        existing_zip.extractall(path=upload_path)

    #DB更新
    RoomOperation.add_entry(
        id=room_id,
        author=author,
        title=title,
        description=description
    )

    author_name = UserOperation.get_name_from_id(author)

    return jsonify([room_id, request.form['title'], request.form['description'], author_name]), 200



# jsonでroom_infoテーブルを上から10個返すAPI
@app.route('/get_list', methods=['GET', 'POST'])
def get_list():
    table = RoomOperation.get_latest_n(1)
    data_list = []
    for row in table:
        author_name = UserOperation.get_name_from_id(row.author)
        data = [row.id, row.title, row.description, author_name]
        data_list.append(data)
    return jsonify(data_list)


if __name__ == "__main__":
    app.run()

