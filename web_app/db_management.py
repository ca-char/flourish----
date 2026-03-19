import json
from datetime import datetime
from werkzeug.security import generate_password_hash
import os
from web_app.extensions import db
from web_app.models import User, Plant, UserPlant, CareNote
from config import Config
from sqlite3 import Error
from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError
from web_app.extensions import bcrypt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def create_db(reset=True):
    try:
        if reset:
            db.drop_all()
            print("Dropped existing tables")
        
        db.create_all()
        print("Database created with all tables")
    except Exception as e:
        print(f"Error creating tables {e}")


def insert_sample_data():
    try:
        with open(os.path.join(BASE_DIR, "..", "sample_data.json")) as f:
            data = json.load(f)
        # with open("sample_data.json") as f:
        #     data = json.load(f)

        users = []
        for entry in data["users"]:
            user = User(
                user_id=entry["user_id"],
                email=entry["email"],
                password=bcrypt.generate_password_hash(entry["password"]).decode('utf-8'),
                first_name=entry["first_name"],
                is_admin=entry["is_admin"]
            )
            users.append(user)
        db.session.add_all(users)
        db.session.commit()
        print('sample user data inserted')

        plants = []
        for entry in data["plants"]:
            plant = Plant(
                plant_id=entry["plant_id"],
                plant_type=entry["plant_type"],
                water=entry["water"],
                light=entry["light"],
                soil=entry["soil"],
                image_filename=entry["image_filename"]
            ) 
            plants.append(plant)
        db.session.add_all(plants)
        db.session.commit()
        print('sample plants data inserted')

        user_plant_entries = []
        for entry in data["user_plants"]:
            user_plant = UserPlant(
                user_plant_id=entry["user_plant_id"],
                user_id=entry["user_id"],
                plant_id=entry["plant_id"],
                plant_name=entry["plant_name"],
                last_watered=datetime.strptime(entry["last_watered"], "%Y-%m-%d").date(),
                next_watering_date=datetime.strptime(entry["next_watering_date"], "%Y-%m-%d").date()
            )
        
            user_plant_entries.append(user_plant)
        db.session.add_all(user_plant_entries)
        db.session.commit()
        print('sample user plants inserted')

        care_notes = []
        for entry in data["care_notes"]:
            care_note = CareNote(
                care_note_id=entry["care_note_id"],
                user_plant_id=entry["user_plant_id"],
                care_note=entry["care_note"],
                note_date=datetime.strptime(entry["note_date"], "%Y-%m-%d").date()
            )
            care_notes.append(care_note)
        db.session.add_all(care_notes)
        db.session.commit()

        print('sample care notes data inserted')
    except (SQLAlchemyError, KeyError, ValueError) as e:
        print(f"Error inserting sample data {e}")
