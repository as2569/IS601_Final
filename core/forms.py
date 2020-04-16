from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField

class RegisterForm(FlaskForm):
	username= StringField('Username', render_kw={'class':'form-control'})
	password = PasswordField('Password', render_kw={'class':'form-control'})
	submit = SubmitField('Register', render_kw={'class':'form-control'})

class SelectForm(FlaskForm):
	name = StringField('Username', render_kw={'class':'form-control'})
	submit = SubmitField('Select Character', render_kw={'class':'form-control'})

