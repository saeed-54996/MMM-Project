from flask import request, session, redirect, url_for, render_template, flash
import hashlib
from model import db, Users, Images
import os
from init import app
import uuid

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
            return redirect(url_for('home'))
    
    return render_template('signup.html')

def user_profile():
    if 'email' in session:
        pass
    else:
        return redirect(url_for('login_route'))
    return render_template('my-profile.html')


def show_pictures():
    return render_template('pictures.html')

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
            custom_filename = request.form.get('custom_filename')
            description = request.form.get('description')
            category = request.form.get('category')
            tags = request.form.get('tags')
            if file.filename == '':
                flash('No selected file', 'error')
                return redirect(request.url)
            
            
            if file and allowed_file(file.filename):
                if custom_filename:
                    filename = custom_filename + os.path.splitext(file.filename)[1]
                else:
                    filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
                
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                new_image = Images(
                    path=filename,
                    title=custom_filename or filename,
                    description=description,
                    category=category,
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
    return render_template('upload.html')

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
