from flask import request, session, redirect, url_for, render_template, flash
import hashlib
from model import db, Users, Images, Articles,Categories
import os
from init import app,or_
import uuid
from csv_reader import read_csv_to_dict_list
from werkzeug.utils import secure_filename

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
    images = Images.query.filter_by(user_id=usr_id).all()
    articles = Articles.query.filter_by(user_id=usr_id).all()
    user = Users.query.filter_by(id=usr_id).first()
    return render_template('user.html',images=images,articles=articles,user=user)

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
        images = Images.query.filter_by(category_id=category_filter).all()
        categories = Categories.query.filter(or_(Categories.type == 'all', Categories.type == 'image')).all()
    return render_template('pictures.html',images=images,categories=categories)

def show_single_picture(picture_id):
    image = Images.query.filter_by(id=picture_id).first()
    name = image.user.name if image.user else 'Unknown User'
    photographer_id = image.user.id if image.user else '0'
    return render_template('picture.html',path=image.path,title=image.title,des=image.description,category=image.category,tags=image.tags,name=name,id=photographer_id)




#----------------------------------------article system:
def show_articles():
    category_filter = request.args.get('category', 'all')
    if(category_filter=="all"):
        articles = Articles.query.all()
        categories = Categories.query.filter(or_(Categories.type == 'all', Categories.type == 'article')).all()
    else:
        articles = Articles.query.filter_by(category_id=category_filter).all()
        categories = Categories.query.filter(or_(Categories.type == 'all', Categories.type == 'article')).all()
    return render_template('articles.html',articles=articles,categories=categories)


def show_single_article(article_id):
    article = Articles.query.filter_by(id=article_id).first()
    name = article.user.name if article.user else 'Unknown User'
    writer_id = article.user.id if article.user else '0'
    return render_template('article.html',article=article,category=article.category,name=name,writer_id=writer_id)






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

def manage_categories():
    if request.method == 'POST':
        # Handle update category
        for category_id in request.form.getlist('id'):
            if category_id:
                category = Categories.query.get(category_id)
                category.name = request.form[f'name_{category_id}']
                category.type = request.form[f'type_{category_id}']
                category.is_deleted = 1 if request.form.get(f'is_deleted_{category_id}') == 'on' else 0
                db.session.commit()
        
        # Handle add new category
        new_name = request.form.get('new_name')
        new_type = request.form.get('new_type')
        if new_name and new_type:
            new_category = Categories(name=new_name, type=new_type)
            db.session.add(new_category)
            db.session.commit()

        return redirect(url_for('manage_categoris_page'))
    
    # Fetch all categories
    categories = Categories.query.all()
    return render_template('manage-categories.html', categories=categories)

def get_categories():
    return Categories.query.all()

def update_category(category_id, name, type, is_deleted):
    category = Categories.query.get(category_id)
    category.name = name
    category.type = type
    category.is_deleted = is_deleted
    db.session.commit()

def add_category(name, type):
    new_category = Categories(name=name, type=type)
    db.session.add(new_category)
    db.session.commit()


# ------------------------------------------upload a csv file in csv folder
def csv_upload():
    if 'user_id' not in session:
        flash('You need to be logged in to import articles', 'error')
        return redirect(url_for('login_route'))

    if request.method == 'POST':
        if 'articles_file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)

        file = request.files['articles_file']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)

        if file and allowed_csv_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('csv', filename))
            flash('File successfully uploaded', 'success')
            if filename == 'articles.csv':
                upload_csv('article')
            if filename == 'images.csv':
                upload_csv('image')

            return redirect(url_for('admin_page'))  # Ensure this redirects to a valid route

    return render_template('admin.html')


def allowed_csv_file(filename):
    ALLOWED_EXTENSIONS = {'csv'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def file_exist(filepath,filename):
    file_path = os.path.join(filepath, filename)
    return os.path.exists(file_path)

def upload_csv(file):


    if file == 'article':
        temp_dict = read_csv_to_dict_list('csv/articles.csv')
        for row in temp_dict:
            user = Users.query.filter_by(email=row['writer_email']).first()

            if not user:
                name = row['writer_name']
                email = row['writer_email']
                password = '123456'
                category = Categories.query.filter_by(name=row['category']).first()
                new_user = Users(name=name, email=email, password=generate_md5_hash(password))
                db.session.add(new_user)
                db.session.commit()
            category = Categories.query.filter_by(name=row['category']).first()
            if not category:
                name = row['category']
                type = 'article'
                new_category = Categories(name=name, type=type, is_deleted=0) 
                db.session.add(new_category)
                db.session.commit()
            elif category.type == 'image':
                category.type = 'all'
                db.session.commit()

            

        for row in temp_dict:
            user = Users.query.filter_by(email=row['writer_email']).first()
            category = Categories.query.filter_by(name=row['category']).first()
            new_article = Articles(
                title=row['title'],
                content=row['content'],
                category_id=category.id,
                keywords=row['keywords'],
                user_id=user.id
            )
            db.session.add(new_article)
            db.session.commit()



    elif file == 'image':
        temp_dict = read_csv_to_dict_list('csv/images.csv')

        for row in temp_dict:
            user = Users.query.filter_by(email=row['photographer_email']).first()
            if not user:
                name = row['writer_name']
                email = row['writer_email']
                password = '123456'

                new_user = Users(name=name, email=email, password=generate_md5_hash(password))
                db.session.add(new_user)
                db.session.commit()
            
            category = Categories.query.filter_by(name=row['category']).first()
            if not category:
                name = row['category']
                type = 'image'
                new_category = Categories(name=name, type=type, is_deleted=0) 
                db.session.add(new_category)
                db.session.commit()
            elif category.type == 'article':
                category.type = 'all'
                db.session.commit()


            
        for row in temp_dict:
            user = Users.query.filter_by(email=row['photographer_email']).first()
            category = Categories.query.filter_by(name=row['category']).first()

            new_image = Images(
                title=row['title'],
                path=row['image_path'],
                tags=row['tags'],
                description=row['description'],
                category_id=category.id,
                user_id=user.id
            )
            db.session.add(new_image)
            db.session.commit()
