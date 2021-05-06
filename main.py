from flask import Flask, request, make_response, redirect, render_template, session, current_app, g, url_for, flash
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import unittest

app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = 'SUPER SECRETO'
app.config['WTF_CSRF_ENABLED']= False

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()]) 
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html', error=error)

@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect("/hello"))
    session['user_ip'] = user_ip

    return response

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    todos = ['TODO 1','TODO 2','TODO 3']
    user_ip = session.get('user_ip')
    login_form = LoginForm()
    username = session.get('username')

    context = {
        "user_ip":user_ip,
        "todos":todos,
        "login_form": login_form, 
        "username": username
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        session['username'] = username

        flash("Username registered successfully!")
        return redirect(url_for('index'))

    return render_template('hello.html', **context)

if __name__ == '__main__':
    app.run()