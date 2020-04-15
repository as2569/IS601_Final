import functools
from flask import Flask, redirect, flash, url_for
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

login_manager = LoginManager()
login_manager.login_view = "auth.login"

def test():
	print('this is a test')

def create_app():
	app = Flask(__name__)

	app.config['SECRET_KEY'] = 'secret'
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	register_extensions(app)
	register_blueprints(app)
	setup_scheduler()

	return app

def setup_scheduler():
	scheduler = BackgroundScheduler()
	scheduler.start()
	scheduler.add_job(
		func=test,
		trigger=IntervalTrigger(seconds=30),
		id='test',
		name='test',
		replace_existing=True)
	atexit.register(lambda: scheduler.shutdown())

def register_extensions(app):
	db.init_app(app)
	migrate.init_app(app, db)
	csrf.init_app(app)
	login_manager.init_app(app)

def register_blueprints(app):
	from final.auth.models import User
	from final.core.models import Character

	@login_manager.user_loader
	def load_user(user_id):
		return User.query.get(int(user_id))

	from final.auth.auth import auth_bp
	from final.core.core import core_bp

	app.register_blueprint(auth_bp)
	app.register_blueprint(core_bp)

def setup_database(app):
	with app.app_context():
		db.create_all()
	db.session.commit()

if __name__ == "__main__":
	app = create_app()
	setup_database(app)
