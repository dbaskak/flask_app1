from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from flask.views import View

db = SQLAlchemy()
app = Flask(__name__)

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '11223344'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .event.views import event_bp
    from .user.views import user_bp
    from .main.views import main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(event_bp)

    return app

class ListView(View):
    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self):
        objects = []

        return render_template(self.template_name, objects=objects)

class DetailView(View):
    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self, id):
        obj = None

        return render_template(self.template_name, obj=obj)

app.add_url_rule('/class/list', view_func=ListView.as_view('list', template_name='list.html'))
app.add_url_rule('/class/detail/<int:id>', view_func=DetailView.as_view('detail', template_name='detail.html'))

if __name__ == '__main__':
    app.run(debug=True)