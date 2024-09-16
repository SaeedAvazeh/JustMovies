pip install Flask python-dateutil
pip install flask-sqlalchemy mysqlclient
pip install flask-bcrypt
pip install flask-login

from flask import Flask
from flask import SQLAlchemy
from flask import Bcrypt
from flask import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFyemxpZXJrd3J0d3Z1dHhjendxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjYwOTIwMjcsImV4cCI6MjA0MTY2ODAyN30.KHsyDuw9y3QmKxDo9qhZ8XXehhTXyRmY8B82PvoFcnM'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.arzlierkwrtwvutxczwq:edAQB4Ji-j669yD@aws-0-eu-central-1.pooler.supabase.com:6543/postgres'
    db.init_app(app)

    from src import model
    from src import main
    from src import auth
    from src import manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        return model.User.query.get(int(user_id))
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(manager.bp)
    with app.app_context():
        db.create_all()

    return app
