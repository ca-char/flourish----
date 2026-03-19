import re

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, HiddenField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, Regexp, ValidationError
from datetime import date

class AddUserPlantForm(FlaskForm):
    plant_name = StringField("Plant Name", validators=[
        DataRequired(), Length(min=2, max=100)
    ])
    plant_id = SelectField("Select Plant", coerce=int, validators=[DataRequired()])
    last_watered = DateField("Last Watered", format="%Y-%m-%d", validators=[DataRequired()])
    care_note = StringField("Care Note", validators=[Optional(), Length(max=255)])
    submit = SubmitField("Submit")


class EditUserPlantForm(FlaskForm):
    plant_id = HiddenField("Plant ID")
    plant_name = StringField("Plant Name", validators=[DataRequired(), Length(min=2, max=100)])
    selected_plant_id = SelectField("Select Plant Type", coerce=int, validators=[DataRequired()])
    last_watered = DateField("Last Watered", format="%Y-%m-%d", validators=[DataRequired()])
    care_note = StringField("Care Note", validators=[Optional(), Length(max=255)])
    submit = SubmitField("Save changes")


class PlantLibraryForm(FlaskForm):
    plant_type = StringField("Plant Type", validators=[DataRequired(), Length(min=2, max=100)])
    water = StringField("Water", validators=[DataRequired(), Length(max=100)])
    light = StringField("Light", validators=[DataRequired(), Length(max=100)])
    soil = StringField("Soil", validators=[DataRequired(), Length(max=100)])
    submit = SubmitField("Save changes")

class DeletePlantForm(FlaskForm):
    plant_id = HiddenField()
    submit = SubmitField('Delete')


class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), Length(min=2, max=100), Regexp(r'^[a-zA-Z\s\-\']+$', 
    message="First name can only contain letters, spaces, hyphens and apostrophes")])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=254)])
    password1 = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=128)])
    password2 = PasswordField("Confirm Password", validators=[
        DataRequired(), EqualTo("password1", message="Passwords must match")
    ])
    submit = SubmitField("Sign up")
    
    def validate_first_name(self, field):
        dangerous_patterns = ["<", ">", ";", "--", "/*", "*/", "DROP", "SELECT", "INSERT"]
        for pattern in dangerous_patterns:
            if pattern.lower() in field.data.lower():
                raise ValidationError("First name contains invalid characters")

    def validate_password1(self, field):
        password = field.data
        if not re.search(r"[A-Z]", password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"[0-9]", password):
            raise ValidationError("Password must contain at least one number.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError("Password must contain at least one special character.")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

class LogoutForm(FlaskForm):
    submit = SubmitField("Log Out")