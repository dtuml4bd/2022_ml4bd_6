import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, predictForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from pickle import load
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
loaded_model = load(open('C:/Users/asus/Downloads/test/flaskblog/predict.pkl', 'rb'))
posts = [
    {
        'author': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS5qdHZXsHVas1os78mfUJNy9Bz7HD2rk0_1PMsZaPybfL8AupvruQpjV9igQKKFXBWg1o&usqp=CAU" alt="Card image cap',
        'title': '150.000 VND',
        'content': 'Buy now',
        'date_posted': 'Shirt'
    }
    ,
    {
        'author': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSn6pbfR0D8MH-2soZTQuf9QkG57eviJhPhMg&usqp=CAU',
        'title': '100.000 VND',
        'content': 'Buy now',
        'date_posted': 'Shorts'
    }
    ,
    {
        'author': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTGBQprPOW8fEcVjUOmOpAFJnYZR9zGIpS00Q&usqp=CAU',
        'title': '120.000 VND',
        'content': 'Buy now',
        'date_posted': 'T-Shirt'
    }
    ,
    {
        'author': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRbpI3MPhXM9twEtgJoxp-nn4e8Sai4u7DWLQ&usqp=CAU',
        'title': '100.000 VND',
        'content': 'Buy now',
        'date_posted': 'Shorts'
    }
    ,
    {
        'author': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSkdKSdqruxNrxICjJeb7zjkwElGjuDYY5Q5_XUXB2eVIOZf9_Ia6bAQ1KR7_v_miQdFsw&usqp=CAU',
        'title': '100.000 VND',
        'content': 'Buy now',
        'date_posted': 'Shorts'
    }
    ,
    {
        'author': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTjosrNFQdOcWXmbXjRtzp0l6iMkP6Fu_gNuw&usqp=CAU',
        'title': '100.000 VND',
        'content': 'Buy now',
        'date_posted': 'Shorts'
    }
    ,
    {
        'author': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQHzAtL8sgSDUgErF7puMuduRaDnripxen62w&usqp=CAU',
        'title': '100.000 VND',
        'content': 'Buy now',
        'date_posted': 'Shorts'
    }
    ,
    {
        'author': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQhCviIiBHQwVJMgWrBdswbwBEbMcHLt9Fz8g&usqp=CAU',
        'title': '100.000 VND',
        'content': 'Buy now',
        'date_posted': 'Shorts'
    }
    ,
    {
        'author': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTGiGc-HVIhIL5vYuzxBH0_1bYOk_CaQBmacQ&usqp=CAU',
        'title': '100.000 VND',
        'content': 'Buy now',
        'date_posted': 'Shorts'
    }
    ,
    {
        'author': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSgeQHy9tDHBNeeAZ3288f6qSm__l-pIHjxeg&usqp=CAU',
        'title': '100.000 VND',
        'content': 'Buy now',
        'date_posted': 'Shorts'
    }
    ,
    {
        'author': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRO5b4HQthLOPL5I17wun5nQD3jTVe3gWizxA&usqp=CAU',
        'title': '100.000 VND',
        'content': 'Buy now',
        'date_posted': 'Shorts'
    }
    ,
    {
        'author': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR6qHmEtJ0Cz7HNCvSkHIClFJft0EM-mjAb9g&usqp=CAU',
        'title': '100.000 VND',
        'content': 'Buy now',
        'date_posted': 'Shorts'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

@app.route("/predict", methods=['GET', 'POST'])
@login_required
def predict():
    
    form = predictForm()
    if form.validate_on_submit():
        decision = "" 
        a = int(form.weight.data)
        b = int(form.age.data)
        c = int(form.height.data)
        dulieu = [a,b,c]
        x_pred_sample1 = np.array(dulieu).reshape(1,-1)
        t = loaded_model.predict(x_pred_sample1)
        if t == 1: 
            decision ="XXS" 
        if t ==2:
            decision ="S" 
        if t ==3:
            decision ="L" 
        if t ==4: 
            decision ="M" 
        if t ==5:
            decision ="X"  
        if t ==6:
            decision ="XXL"  
        flash(f'The recommended size for you is {decision}', 'success')
    return render_template('predict.html',form=form)
        