from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from scalper import app, db, RECAPTCHA_SECRET_KEY
from scalper.models import User
import json
import requests


@app.route('/', methods=['GET'])
def auth_and_register():
    return render_template('index.html')


@app.route('/main', methods=['GET'])
@login_required
def main():
    return render_template('main.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    email = request.form.get('email')
    password = request.form.get('password')

    if email and password:
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            rm = True if request.form.get('remainme') else False
            login_user(user, remember=rm)
            return redirect(url_for('main'))
        else:
            flash('Неверный логин или пароль')
    else:
        flash('Пожалуйста, заполните все поля')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    if request.method == 'POST':  # FIXME
        captcha_response = request.form['g-recaptcha-response']
        if not (email or password or password2):
            flash('Пожалуйста, заполните все поля')
        if User.query.filter_by(email=email).first():
            flash('Данный email зарегистрирован')
        elif len(password) < 8:
            flash('Минимальная длина пароля: 8 ')
        elif password != password2:
            flash('Пароли не совпадают')
        elif cap_check(captcha_response):
            hash_pwd = generate_password_hash(password)
            new_user = User(email=email, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login_page'))
        else:
            flash("Пройдите проверку")

    return render_template('register.html')


def cap_check(captcha_response):
    payload = {'response': captcha_response, 'secret': RECAPTCHA_SECRET_KEY}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json.loads(response.text)
    return response_text['success']  # Returns True captcha test passed for submitted form else returns False.


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_and_register'))
