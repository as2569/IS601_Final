from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from final.auth.forms import RegisterForm, LoginForm
from final.auth.models import User
#from app import db

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		username = request.form.get('username')
		password = request.form.get('password')
		remember = True if request.form.get('remember') else False

		user = User.query.filter_by(username=username).first()

		if user is None or not user.check_password_hash(user.password, password):
			flash('Invalid username or password')
			return redirect(url_for('auth.login'))

		login_user(user, remember)
		return redirect(url_for('core.index'))

	return render_template('login.html', title='Sign In', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('core.index'))


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
	form = RegisterForm()
	if form.validate_on_submit():
		username = request.form.get('username')
		password = request.form.get('password')

		user = User.query.filter_by(username=username).first()

		if user:
			flask('User already exists')
			return redirect(url_for('auth.signup'))

		new_user = User(username=username, password=generate_password_hash(password, method='sha256'))
		db.session.add(new_user)
		db.session.commit()
		return redirect(url_for('auth.login'))
	return render_template('signup.html', form=form)
