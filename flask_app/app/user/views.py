from flask import Blueprint, render_template, jsonify
from .models import User
from flask import current_app as app

user_bp = Blueprint('user', __name__, template_folder='templates/user')

@user_bp.route('/api/users')
def api_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users])

@user_bp.route('/users')
def users_list():
    users = User.query.all()
    return render_template('users.html', users=users)
