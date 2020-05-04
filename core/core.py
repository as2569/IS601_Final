from flask import Blueprint, render_template, url_for, redirect, request, current_app
from flask_login import current_user, login_required
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit

from final.core.forms import SelectForm
from final.core.models import Character
from final.app import db

core_bp = Blueprint('core', __name__, template_folder='templates')

@core_bp.route('/')
@login_required
def index():
	character = Character.query.filter_by(owner_id=current_user.get_id()).first()

	if character is None:
		# First character, go to create character
		return redirect(url_for('core.selectCharacter'))
	if character.alive is False:
		# Dead character, go to create character
		return redirect(url_for('core.selectCharacter'))

	setupScheduler()
	character = Character.query.filter_by(owner_id=current_user.get_id()).first()
	return render_template('index.html', character = character)

@core_bp.route('/selectCharacter', methods=['GET', 'POST'])
@login_required
def selectCharacter():
	form = SelectForm()
	if form.validate_on_submit():
		character = Character()
		character.owner_id=current_user.get_id()
		character.alive=True
		character.energy=50
		character.sanity=50
		character.money=50
		character.characterName=request.form.get('name')

		db.session.add(character)
		db.session.commit()
		return redirect(url_for('core.index'))
	return render_template('selectCharacter.html', form=form)

@core_bp.route('/updateCharacter')
@login_required
def updateCharacter():
	character = Character.query.filter_by(owner_id=current_user.get_id()).first()
	character.money = character.money - 10
	db.session.commit()
	return render_template('index.html', character = character)

def test():
	print('test')

def setupScheduler():
	scheduler = BackgroundScheduler()
	scheduler.add_job(
		func=test,
		trigger=IntervalTrigger(seconds=15))
	scheduler.start()
	atexit.register(lambda: scheduler.shutdown())
