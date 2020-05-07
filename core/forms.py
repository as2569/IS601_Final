from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField

class SelectForm(FlaskForm):
	name = StringField('Username', render_kw={'class':'form-control'})
	submit = SubmitField('Select Character', render_kw={'class':'form-control'})

