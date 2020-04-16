from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import current_user, login_required

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
		print('char is none')
		return redirect(url_for('core.selectCharacter'))

	if character.alive is False:
		# Dead character, go to create character
		print('char exists')
		return redirect(url_for('core.selectCharacter'))

	return render_template('index.html')

@core_bp.route('/selectCharacter', methods=['GET', 'POST'])
@login_required
def selectCharacter():
	form = SelectForm()
	if form.validate_on_submit():
		name = request.form.get('name')
		print('select character name ' + name)
	return render_template('selectCharacter.html', form=form)
