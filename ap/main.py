from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
import random
import zipfile
import tempfile

import logging

from werkzeug.utils import send_from_directory

logging.basicConfig(filename='/var/log/python.log', level=logging.DEBUG)

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = app.root_path + "/static"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db_uri = "sqlite:///" + os.path.join(app.root_path, 'oshikabe.db')
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

db = SQLAlchemy(app) 

class Entry(db.Model): 
    __tablename__ = "room_info" 
    room_id = db.Column(db.String(), primary_key=True) # 自動でランダム値を。authorが付けれるようにしてもいいかも(使用可能判定が必要)
    room_name = db.Column(db.String(), nullable=False) # タイトル。authorが自由につける
    room_path = db.Column(db.String(), nullable=False)
    author = db.Column(db.String(), nullable=False)

db.create_all()

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/upload_page', methods=['GET', 'POST'])
def upload_page():
    return render_template("upload_page.html")

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    print("upload entered")
    if request.method == 'POST':

        room_id = random.uniform(100, 200)

        room_name = request.form['room_name']

        file = request.files['zip_input']
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], room_name)
        with zipfile.ZipFile(file) as existing_zip:
            filename = existing_zip.namelist()[0]
            existing_zip.extractall(path=upload_path)
        room_path = room_name + "/" + filename

        author = request.form['author']

        add_entry(
            room_id,
            room_name,
            room_path,
            author
        )
    return "uploaded"

@app.route('/room', methods=['POST', 'GET'])
def room():
    room_name = request.args.get('room_name')
    if is_exist(room_name):
        entry = Entry.query.filter(Entry.room_name == request.args.get('room_name') ).first()
        print(entry.room_path)
        return send_from_directory(entry.room_path, 'index.html')
        #return app.send_static_file(entry.room_path + "index.html")
    else:
        return "NG"

def add_entry(room_id, room_name, room_path, author):
    entry = Entry()
    entry.room_id = room_id
    entry.room_name = room_name
    entry.room_path = room_path
    entry.author = author

    db.session.add(entry)
    db.session.commit()
    return 0

def is_exist(room_name):
    table = Entry.query.all()
    for row in table:
        if row.room_name == room_name:
            return True
    return False


if __name__ == "__main__":
    app.run()