from database import db

# これがModel
class Room(db.Model): 
    __tablename__ = "room_info" 
    id = db.Column(db.String(), nullable=False, primary_key=True) #id=room_name
    author = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(), nullable=True)
    description = db.Column(db.String(), nullable=True)

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