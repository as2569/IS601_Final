from flask import Blueprint, render_template, url_for, redirect, request, current_app
from flask_login import current_user, login_required
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit

from final.core.forms import SelectForm
from final.core.models import Character
from final.app import db, scheduler

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
	if(checkLoseCondition() is True):
		# Lose condition triggered, go to game over
		return redirect(url_for('core.gameOver'))

	character = Character.query.filter_by(owner_id=current_user.get_id()).first()
	return render_template('index.html', character = character)

def checkLoseCondition():
	character = Character.query.filter_by(owner_id=current_user.get_id()).first()
	if character.money <= 0:
		print("no money, gameover")
		return True
	return False

@scheduler.task('interval', id='random', seconds=20)
def job():
	print('Job test')

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

@core_bp.route('/gameOver')
def gameOver():
	#todo shutdown scheduler
	print('game over')
	character = Character.query.filter_by(owner_id=current_user.get_id()).first()
	db.session.delete(character)
	db.session.commit()
	return render_template('gameOver.html', character = character)

@core_bp.route('/allowNap')
@login_required
def allowNap():
	print('allow nap')
	character = Character.query.filter_by(owner_id=current_user.get_id()).first()
	character.money = character.money - 10
	db.session.commit()
	return render_template('index.html', character = character)

@core_bp.route('/buyCoffee')
@login_required
def buyCoffee():
	print('buy coffee')
	character = Character.query.filter_by(owner_id=current_user.get_id()).first()
	if(character.money > -10):
		character.money = character.money - 2
		character.energy = character.energy + 3
		db.session.commit()
	return redirect(url_for('core.index'))

@core_bp.route('/updateCharacter')
@login_required
def updateCharacter():
        print('updating character')
        character = Character.query.filter_by(owner_id=current_user.get_id()).first()
        character.money = character.money - 10
        db.session.commit()
        return render_template('index.html', character = character)

