from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

db_uri = "sqlite:///" + os.path.join(app.root_path, 'yurikabe.db')
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

db = SQLAlchemy(app) 
db.create_all()

# これがModel
class Room(db.Model): 
    __tablename__ = "room_info" 
    id = db.Column(db.String(), nullable=False, primary_key=True) #id=room_name
    author = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(), nullable=True)
    description = db.Column(db.String(), nullable=True)
    tags = db.Column(db.String(), nullable=True)

# こっからメソッド
def add_entry(id, author, title, description, tags):
    entry = Room()
    entry.id = id
    entry.author = author
    entry.title = title
    entry.description = description
    entry.tags = tags

    db.session.add(entry)
    db.session.commit()
    return 0

def is_exist(id):
    table = Room.query.all()
    for row in table:
        if row.name == id:
            return True
    return False

def get_latest_n(n):
    table = Room.query.order_by(Room.id).get(n) #order_by(date)にしたい
    return table