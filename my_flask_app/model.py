# models.py
from app import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.column(db.string(5), unique=True, nullable=False)
    author_and_photographer = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.column(db.txt , nullable=False)


    def __repr__(self):
        return f'<User {self.username}>'
    
class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.txt, nullable=False)
    keywords = db.Column(db.str(50))
    title = db.Column(db.str(50))
    category = db.Column(db.str(50))
    writer_code = db.Column(db.str(50), nullable=False)
    writer_name = db.Column(db.str(50), nullable=False)
    writer_email = db.Column(db.str(50))

class Photographer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.txt, nullable=False)
    title = db.Column(db.str(50))
    tag = db.Column(db.str(50))
    discription = db.Column(db.str(120))
    category = db.Column(db.str(50))
    photographer_code = db.Column(db.str(50), nullable=False)
    photographer_name = db.Column(db.str(50), nullable=False)
    photographer_email = db.Column(db.str(50))