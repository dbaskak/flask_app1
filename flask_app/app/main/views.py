from flask import Blueprint, render_template, request, redirect, session, url_for
from functools import wraps
from flask_app.app.user.models import User
from flask_app.app import db
from .forms import UserForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.login_page'))
    return render_template('register.html', form=form)

@main_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['username'] = username
            return redirect(url_for('event.events'))
        else:
            return render_template('unauthorized.html'), 401
    else:
        return render_template('main/login.html')

@main_bp.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('main.login_page'))

def login_required(route_function):
    @wraps(route_function)
    def decorated_route(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('main.login_page'))
        return route_function(*args, **kwargs)
    return decorated_route

@main_bp.route('/events')
@login_required
def events():
    return render_template('events.html')

@main_bp.route('/users')
@login_required
def users():
    return render_template('event_users.html')
