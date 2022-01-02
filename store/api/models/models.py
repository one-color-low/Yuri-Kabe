from os import name
from posix import RTLD_NODELETE
from database import db

# これがModel
class Room(db.Model): 
    __tablename__ = "room_info" 
    id = db.Column(db.String(), nullable=False, primary_key=True) #id=room_name
    author = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(), nullable=True)
    description = db.Column(db.String(), nullable=True)

class User(db.Model): 
    __tablename__ = "user_info" 
    id = db.Column(db.String(), nullable=False, primary_key=True) 
    name = db.Column(db.String(), nullable=False)
    token = db.Column(db.String(), nullable=True)

# こっからメソッド
class RoomOperation():
    def add_entry(id, author, title, description):
        entry = Room()
        entry.id = id
        entry.author = author
        entry.title = title
        entry.description = description

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
        table = db.session.query(Room).all()
        return table
    
class UserOperation():
    def add_entry(id, name, token):
        entry = User()
        entry.id = id
        entry.name = name
        entry.token = token

        db.session.add(entry)
        db.session.commit()
        return 0

    def is_exist(id):
        table = User.query.all()
        for row in table:
            if row.id == id:
                return True
        return False

    def get_latest_n(n):
        table = db.session.query(User).all()
        return table

    def get_id_from_token(token):
        table = User.query.all()
        for row in table:
            if row.token == token:
                print("ok")
                return row.id
        return "user id not found."