from final.app import db

class Character(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	alive = db.Column(db.Boolean)
	characterName = db.Column(db.String(100), unique=True)
	energy = db.Column(db.Integer)
	sanity = db.Column(db.Integer)
	money = db.Column(db.Integer)
	grades = db.Column(db.Integer)
	progress = db.Column(db.Integer)
	owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class EventRecord(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	timeStamp = db.Column(db.DateTime)
	event = db.Column(db.String(200))
	owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
