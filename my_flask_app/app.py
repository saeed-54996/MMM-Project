from flask import *
from init import app, db 
from model import *
from controler import login, signup ,upload_photo,user_profile,show_pictures,show_single_picture,submit_article,admin_panel

@app.route('/')
def home():
    if 'email' in session and 'user_id' in session:
        return render_template('index.html', email=session['email'], user_id=session['user_id'])
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
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/my-profile/')
def my_profile():
    return user_profile()

@app.route('/pictures/',methods=['GET'])
def pictures():
    return show_pictures()

@app.route('/picture/<picture_id>/')
def picture(picture_id):
    return show_single_picture(picture_id)

@app.route('/articles/')
def articles_page():
    return render_template('articles.html')

@app.route('/article/<article_id>/')
def singel_article_page(article_id):
    return render_template('article.html')

@app.route('/writer-photographer/')
def writer_photographer():
    return render_template('writer-photographer.html')

@app.route('/upload/', methods=['GET', 'POST'])
def upload_route():
    return upload_photo()

@app.route('/submit-article/', methods=['GET', 'POST'])
def submit_article_route():
    return submit_article()

@app.route('/admin/', methods=['POST', 'GET'])
def admin_page():
    return admin_panel()


if __name__ == '__main__':
    app.run(port=5000, debug=True)
