from datetime import datetime
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from forms import EventForm
from flask_app.app.event.models import Event, EventUser
from flask_app.app.database import db
from flask_app.app.user.models import User
from flask_app import app


event_bp = Blueprint('event', __name__, template_folder='templates/event')
user_bp = Blueprint('user', __name__, template_folder='templates/user')

@event_bp.route('/events', methods=['GET'])
def get_events():
    title = request.args.get('title')
    events = Event.query.filter(Event.title.ilike(f"%{title}%")).all() if title else Event.query.all()
    return render_template('events.html', events=events)

@event_bp.route('/events', methods=['GET'])
def get_events_with_pagination():
    page = request.args.get('page', default=1, type=int)
    size = request.args.get('size', default=10, type=int)
    events = Event.query.paginate(page=page, per_page=size)
    return render_template('events.html', events=events)

@event_bp.route('/events', methods=['GET'])
def get_upcoming_events():
    current_user_id = session.get('user_id')
    events = Event.query.filter(Event.end_date > datetime.now()).all()
    for event in events:
        if len(event.users) >= event.capacity:
            event.full = True
        if current_user_id in [user.id for user in event.users]:
            event.registered = True
    return render_template('events.html', events=events)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['username'] = username
        return redirect(url_for('events'))
    else:
        return 'Unauthorized', 401

@event_bp.route('/events/create', methods=['GET', 'POST'])
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(title=form.title.data, description=form.description.data, date=form.date.data, location=form.location.data)
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('events'))
    return render_template('create.html', form=form)

@event_bp.route('/events/<int:id>')
def event_detail(id):
    event = Event.query.get(id)
    return render_template('event_users.html', event=event)

@event_bp.route('/events/<int:id>/update', methods=['GET', 'POST'])
def update_event(id):
    event = Event.query.get(id)
    form = EventForm(obj=event)
    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.date = form.date.data
        event.location = form.location.data
        db.session.commit()
        return redirect(url_for('event_detail', id=event.id))
    return render_template('update.html', form=form, event=event)

@event_bp.route('/events/<int:id>/users')
def event_users(id):
    event_users = EventUser.query.filter_by(event_id=id).all()
    return render_template('event_users.html', event_users=event_users)

@event_bp.route('/api/events/<int:id>/users')
def api_event_users(id):
    event_users = EventUser.query.filter_by(event_id=id).all()
    return jsonify([event_user.serialize() for event_user in event_users])

@event_bp.route('/api/events')
def api_events():
    events = Event.query.all()
    return jsonify([event.serialize() for event in events])

@app.route('/class/events')
def class_events():
    return render_template('events.html')

@app.route('/class/events/<int:id>')
def class_event_detail(id):
    return render_template('detail.html', id=id)

@app.route('/class/users')
def class_users():
    return render_template('')


@app.route('/class/users/<int:id>')
def class_user_detail(id):
    return render_template('detail.html', id=id)
