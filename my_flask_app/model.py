from init import db

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=True)
    # Relationship to Articles
    articles = db.relationship('Articles', backref='user', lazy=True)
    # Relationship to Images
    images = db.relationship('Images', backref='user', lazy=True)

class Articles(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120), nullable=True)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=True)
    keywords = db.Column(db.Text, nullable=True)
    # Foreign key linking to Users table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Images(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    path = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(120), nullable=True)
    category = db.Column(db.String(50), nullable=True)
    tags = db.Column(db.String(50), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Categories(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    type = db.Column(db.String(50), nullable=False)
    is_deleted = db.Column(db.Integer, default=0)