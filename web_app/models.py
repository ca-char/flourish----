from web_app.extensions import db
from flask_login import UserMixin
from datetime import datetime, UTC

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    user_plants = db.relationship('UserPlant', backref='user', lazy=True)

    def get_id(self):
        return str(self.user_id)

class Plant(db.Model):
    __tablename__ = 'plant'

    plant_id = db.Column(db.Integer, primary_key=True, nullable=False)
    plant_type = db.Column(db.String(100), unique=True, nullable=False)
    water = db.Column(db.String(100), nullable=False)
    light = db.Column(db.String(100), nullable=False)
    soil = db.Column(db.String(100), nullable=False)
    image_filename = db.Column(db.String(50), nullable=True)

    user_plants = db.relationship('UserPlant', backref='plant', lazy=True)

class UserPlant(db.Model):
    __tablename__ = 'user_plant'

    user_plant_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.plant_id'), nullable=False)
    plant_name = db.Column(db.String(50), nullable=False)
    last_watered = db.Column(db.Date)
    next_watering_date = db.Column(db.Date)

    care_notes = db.relationship('CareNote', backref='user_plant', lazy='dynamic')

class CareNote(db.Model):
    __tablename__ = 'care_note'

    care_note_id = db.Column(db.Integer, primary_key=True)
    user_plant_id = db.Column(db.Integer, db.ForeignKey('user_plant.user_plant_id'), nullable=False)
    care_note = db.Column(db.String(500), nullable=False)
    note_date = db.Column(db.Date, nullable=False, default=datetime.now(UTC))