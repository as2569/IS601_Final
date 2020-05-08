from flask import Blueprint, render_template, url_for, redirect, request, current_app
from flask_login import current_user, login_required
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy import desc
import atexit
import datetime

from final.core.forms import SelectForm
from final.core.models import Character, EventRecord
from final.app import db, scheduler

core_bp = Blueprint('core', __name__, template_folder='templates')

# Page
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
	if(checkLoseCondition() is True):
		# Lose condition triggered, go to game over
		return redirect(url_for('core.gameOver'))

	character = Character.query.filter_by(owner_id=current_user.get_id()).first()
	return render_template('index.html', character = character, records = getEventRecords())

# Utility
def checkLoseCondition():
	character = Character.query.filter_by(owner_id=current_user.get_id()).first()
	if character.money <= 0:
		print("no money, gameover")
		return True
	return False

# Utility
def addEventRecord(str):
	eventRecord = EventRecord()
	eventRecord.owner_id = current_user.get_id()
	eventRecord.event = str
	eventRecord.timeStamp = datetime.datetime.now()

	db.session.add(eventRecord)
	db.session.commit()

	getEventRecords()

# Utility
def getEventRecords():
	rList = EventRecord.query.filter_by(owner_id=current_user.get_id()).order_by(desc(EventRecord.timeStamp)).limit(100)
	return rList

# Task
@scheduler.task('interval', id='random', seconds=20)
def job():
	print('Job test')

# Page
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
		character.grades=50
		character.progress=50
		character.characterName=request.form.get('name')

		db.session.add(character)
		db.session.commit()
		return redirect(url_for('core.index'))
	return render_template('selectCharacter.html', form=form)

# Page
@core_bp.route('/gameOver')
def gameOver():
	#todo shutdown scheduler
	print('game over')
	character = Character.query.filter_by(owner_id=current_user.get_id()).first()
	db.session.delete(character)
	db.session.commit()
	return render_template('gameOver.html', character = character)

# User
@core_bp.route('/coffee')
@login_required
def coffee():
	print('coffee')
	character = Character.query.filter_by(owner_id=current_user.get_id()).first()
	character.money = character.money - 1
	character.energy = character.energy + 2
	db.session.commit()

	s = 'Bought Coffee. Money -1, Energy +2'
	addEventRecord(s)
	return redirect(url_for('core.index'))

# User
@core_bp.route('/nap')
@login_required
def nap():
	print('nap')
	character = Character.query.filter_by(owner_id=current_user.get_id()).first()
	character.energy = character.energy + 4
	character.sanity = character.sanity + 4
	character.progress = character.progress - 3
	character.grades = character.grades - 3
	db.session.commit()

	s = 'You allow for a nap. Energy +4, Sanity +4, Grades -3, Research -3'
	addEventRecords(s)
	return redirect(url_for('core.index'))

# User
@core_bp.route('/research')
@login_required
def research():
	print('research')
	character = Character.query.filter_by(owner_id=current_user.get_id()).first()
	character.sanity = character.sanity - 2
	character.energy = character.energy - 3
	character.progress = character.progress +6
	db.session.commit()

	s = 'Research. Research +6, Energy -3, Sanity -2'
	addEventRecords(s)
	return redirect(url_for('core.index'))

# User
@core_bp.route('/uber')
@login_required
def uber():
	print('uber')
	character = Character.query.filter_by(owner_id=current_user.get_id()).first()
	character.money = character.money + 5
	character.energy = character.energy - 4
	db.session.commit()

	s = 'Driving Uber. Money +5, Energy -4'
	addEventRecords(s)
	return redirect(url_for('core.index'))

# User
@core_bp.route('/beer')
@login_required
def beer():
	print('beer')
	character = Character.query.filter_by(owner_id=current_user.get_id()).first()
	character.money = character.money - 1
	character.sanity = character.sanity + 2
	db.session.commit()

	s = 'Bought a beer. Sanity +2, Money -1'
	addEventRecords(s)
	return redirect(url_for('core.index'))

# User
@core_bp.route('/study')
@login_required
def study():
	print('study')
	character = Character.query.filter_by(owner_id=current_user.get_id()).first()
	character.grades = character.grades + 6
	character.energy = character.energy - 2
	character.sanity = character.sanity - 3
	db.session.commit()

	s = 'Study. Grades +6, Energy -2, Sanity -3'
	addEventRecords(s)
	return redirect(url_for('core.index'))

# Debug
@core_bp.route('/kill')
@login_required
def kill():
	character = Character.query.filter_by(owner_id=current_user.get_id()).first()
	character.grades = character.grades - 1000
	character.energy = character.energy - 1000
	character.sanity = character.sanity - 1000
	character.progress = character.progress - 1000
	character.money = character.money - 1000
	db.session.commit()
	return redirect(url_for('core.index'))

