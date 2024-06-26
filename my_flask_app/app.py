from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from db_config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy(app)
Migrate = Migrate(app , db)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/picture/')
def picture():
    return render_template("picture.html")

@app.route('/article/')
def article():
    return render_template("article.html")

@app.route('/writer-photographer/')
def writer_photographer():
    return render_template("writer-photographer.html")


if __name__ == '__main__':
    app.run(port=5000, debug=True)
