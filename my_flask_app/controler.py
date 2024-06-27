from flask import request, session, redirect, url_for, render_template, flash
import hashlib
from model import db, Users

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
            return redirect(url_for('home'))
    
    return render_template('signup.html')
