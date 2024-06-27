from flask import *
from init import app, db 
from model import *
from controler import login, signup ,upload_photo

@app.route('/')
def home():
    if 'email' in session:
        return render_template('index.html', email=session['email'])
    return render_template('index.html')

@app.route('/login/', methods=['GET', 'POST'])
def login_route():
    return login()

@app.route('/signup/', methods=['GET', 'POST'])
def signup_route():
    return signup()

@app.route('/logout/')
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))

@app.route('/pictures/')
def pictures():
    return render_template('pictures.html')

@app.route('/picture/<picture_id>/')
def picture(picture_id):
    return render_template('picture.html')

@app.route('/article/')
def article():
    return render_template('article.html')

@app.route('/writer-photographer/')
def writer_photographer():
    return render_template('writer-photographer.html')

@app.route('/upload/', methods=['GET', 'POST'])
def upload_route():
    return upload_photo()

if __name__ == '__main__':
    app.run(port=5000, debug=True)
