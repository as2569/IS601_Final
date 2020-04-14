from flask import Blueprint, render_template
from flask_login import current_user, login_required

core_bp = Blueprint('core', __name__, template_folder='templates')

@core_bp.route('/')
def index():
	return render_template('index.html')

