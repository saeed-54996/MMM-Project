from flask import request, session, redirect, url_for, render_template, flash
import hashlib
from model import db, Users, Images, Articles,Categories
import os
from init import app,or_
import uuid
import csv
import csv_reader

#----------------------------------------login system:
def generate_md5_hash(password):
    return hashlib.md5(password.encode()).hexdigest()

def check_md5_hash(password, hash):
    return generate_md5_hash(password) == hash

def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = Users.query.filter_by(email=email).first()
        if user and check_md5_hash(password, user.password):
            session['email'] = user.email
            session['user_id'] = user.id
            session['name'] = user.name
            session['role'] = user.role
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('signup.html')

        user = Users.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists', 'error')
            return render_template('signup.html')
        else:
            new_user = Users(name=name, email=email, password=generate_md5_hash(password))
            db.session.add(new_user)
            db.session.commit()
            session['email'] = new_user.email
            session['user_id'] = new_user.id
            session['name'] = new_user.name
            session['role'] = new_user.role
            return redirect(url_for('home'))
    
    return render_template('signup.html')




#----------------------------------------profile and Admin system:
def dashboard():
    if 'email' in session:
        pass
    else:
        return redirect(url_for('login_route'))
    return render_template('my-profile.html')

def user_profile(usr_id):
    return render_template('user.html')

def show_users():
    users = Users.query.all()
    return render_template('writer-photographer.html',users=users)


#----------------------------------------image system:
def show_pictures():
    category_filter = request.args.get('category', 'all')
    if(category_filter=="all"):
        images = Images.query.all()
        categories = Categories.query.filter(or_(Categories.type == 'all', Categories.type == 'image')).all()
    else:
        images = Images.query.filter_by(category_id=category_filter)
        categories = Categories.query.filter(or_(Categories.type == 'all', Categories.type == 'image')).all()
    return render_template('pictures.html',images=images,categories=categories)

def show_single_picture(picture_id):
    image = Images.query.filter_by(id=picture_id).first()
    name = image.user.name if image.user else 'Unknown User'
    return render_template('picture.html',path=image.path,title=image.title,des=image.description,category=image.category.name,tags=image.tags,name=name)




#----------------------------------------article system:
def show_articles():
    articles = Articles.query.all()
    return render_template('articles.html',articles=articles)


def show_single_article(article_id):
    return render_template('article.html')






#----------------------------------------submit sytsem:
def submit_article():
    if 'user_id' not in session:
        flash('You need to be logged in to submit an article', 'error')
        return redirect(url_for('login_route'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category')
        keywords = request.form.get('keywords')
        
        if not title or not content:
            flash('Title and content are required', 'error')
            return redirect(url_for('submit_article_route'))
        
        new_article = Articles(
            title=title,
            content=content,
            category_id=category,
            keywords=keywords,
            user_id=session['user_id']
        )
        db.session.add(new_article)
        db.session.commit()
        
        flash('Article successfully submitted', 'success')
        return redirect(url_for('submit_article_route'))
    

    categories = Categories.query.filter(or_(Categories.type == 'all', Categories.type == 'article')).all()
    return render_template('submit_article.html',categories=categories)

def upload_photo():
    if  not 'user_id' in session:
        flash('user is not loged in')
        return redirect(url_for('login_route'))


    else:
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part', 'error')
                return redirect(request.url)
            
            
            file = request.files['file']
            title = request.form.get('title')
            description = request.form.get('description')
            category = request.form.get('category')
            tags = request.form.get('tags')
            if file.filename == '':
                flash('No selected file', 'error')
                return redirect(request.url)
            
            
            if file and allowed_image_file(file.filename):
                filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
                filetitle = os.path.splitext(file.filename)[0]
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                new_image = Images(
                    path=filename,
                    title=title or filetitle,
                    description=description,
                    category_id=category,
                    tags=tags,
                    user_id = session['user_id']
                )
                db.session.add(new_image)
                db.session.commit()
                
                flash('File successfully uploaded', 'success')
                return redirect(url_for('upload_route'))
            else:
                flash('File type not allowed', 'error')
                return redirect(request.url)
    categories = Categories.query.filter(or_(Categories.type == 'all', Categories.type == 'image')).all()
    return render_template('upload.html',categories=categories)

def allowed_image_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def admin_panel():
    if 'role' in session:
        if session['role'] == 'admin':
            return render_template('admin.html')
        else:
            return redirect(url_for('my_profile'))
    else:
        return redirect(url_for('my_profile'))



def import_articles():
    if 'user_id' not in session:
        flash('You need to be logged in to import articles', 'error')
        return redirect(url_for('login_route'))

    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        
        if file and allowed_csv_file(file.filename):
            try:
                file_content = file.read().decode('utf-8')
                csv_reader = csv.reader(file_content.splitlines())
                for row in csv_reader:
                    if len(row) < 4:
                        continue  # Skip rows that don't have enough columns
                    title, content, category, keywords = row
                    new_article = Articles(
                        title=title,
                        content=content,
                        category=category,
                        keywords=keywords,
                        user_id=session['user_id']
                    )
                    db.session.add(new_article)
                db.session.commit()
                flash('Articles successfully imported', 'success')
            except Exception as e:
                flash(f'An error occurred: {e}', 'error')
            return redirect(url_for('admin_page'))
        else:
            flash('File type not allowed', 'error')
            return redirect(request.url)
    return render_template('admin.html')

def import_images():
    if 'user_id' not in session:
        flash('You need to be logged in to import images', 'error')
        return redirect(url_for('login_route'))
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        
        if file and allowed_csv_file(file.filename):
            try:
                file_content = file.read().decode('utf-8')
                csv_reader = csv.reader(file_content.splitlines())
                for row in csv_reader:
                    if len(row) < 6:
                        continue  # Skip rows that don't have enough columns
                    path, title, tags, description, category, user_id = row
                    new_image = Images(
                        path=path,
                        title=title,
                        tags=tags,
                        description=description,
                        category=category,
                        user_id=session['user_id']
                    )
                    db.session.add(new_image)
                db.session.commit()
                flash('Images successfully imported', 'success')
            except Exception as e:
                flash(f'An error occurred: {e}', 'error')
            return redirect(url_for('admin_page'))
        else:
            flash('File type not allowed', 'error')
            return redirect(request.url)
    return render_template('admin.html')


def allowed_csv_file(filename):
    ALLOWED_EXTENSIONS = {'csv'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

