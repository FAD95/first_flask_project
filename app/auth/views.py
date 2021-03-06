from flask import render_template, session, redirect, flash, url_for
from flask_login import login_user
from app.forms import LoginForm
from app.firestore_service import get_user
from app.models import UserModel, UserData
from app.forms import LoginForm
from . import auth

@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form': login_form 
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict() is not None:
            password_from_db = user_doc.to_dict()['password']

            if password == password_from_db:
                user_data = UserData(username, password)
                user = UserModel(user_data)

                login_user(user)

                flash('Bienvenido de nuevo')

                redirect(url_for('hello'))
            else:
                flash('La informaición no coincide')
        else:
            flash('El usario no existe')

        return redirect(url_for('index'))

    return render_template('login.html', **context)
