from flask import Flask, request, make_response, redirect, render_template, session
import unittest
from flask_login import login_required, current_user
from app.firestore_service import get_users, get_todos
from app import create_app 

app = create_app()

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

@app.route('/hello', methods=['GET'])
@login_required
def hello():
    todos = ['TODO 1','TODO 2','TODO 3']
    user_ip = session.get('user_ip')
    username = current_user.id

    context = {
        "user_ip":user_ip,
        "todos":get_todos(user_id=username),
        "username": username
    }

    users = get_users()

    for user in users:
        print(user.id)
        print(user.to_dict()['password'])

    return render_template('hello.html', **context)

if __name__ == '__main__':
    app.run()