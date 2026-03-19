import logging
from os import abort

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func
from collections import defaultdict
from web_app.models import UserPlant, Plant, User, CareNote
from web_app.extensions import db
from web_app.utils.decorators import regular_user_required, admin_required
from datetime import datetime, timedelta, timezone
from web_app.forms import AddUserPlantForm, EditUserPlantForm, PlantLibraryForm, DeletePlantForm, LogoutForm

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return redirect(url_for('auth.login'))

@views.route('/navigation_base')
@login_required
def navigation_base():
    logout_form = LogoutForm()
    return render_template("navigation_base.html", logout_form=logout_form, user_name=current_user.first_name)

@views.route('/my_plants', methods=['GET', 'POST'])
@login_required
@regular_user_required
def my_plants():
    logout_form = LogoutForm()
    form = AddUserPlantForm()
    form.plant_id.choices = [(p.plant_id, p.plant_type) for p in Plant.query.all()]
    available_plants = Plant.query.all()

    if form.validate_on_submit():
        last_watered_date = form.last_watered.data
        next_watering_date = last_watered_date + timedelta(days=7)

        new_user_plant = UserPlant(
            user_id=current_user.user_id,
            plant_id=form.plant_id.data,
            plant_name=form.plant_name.data,
            last_watered=last_watered_date,
            next_watering_date=next_watering_date
        )
        db.session.add(new_user_plant)
        db.session.commit()

        if form.care_note.data:
            note = CareNote(
                user_plant_id=new_user_plant.user_plant_id,
                care_note=form.care_note.data,
                note_date=datetime.now(timezone.utc).date()
            )
            db.session.add(note)
            db.session.commit()

        flash(f"{new_user_plant.plant_name} added successfully", category="success")
        return redirect(url_for("views.my_plants"))
    elif request.method == "POST":
        flash("Please fix the errors in the form", category="error")

    user_plants = UserPlant.query.filter_by(user_id=current_user.user_id).all()
    notes_for_each_plant = defaultdict(list)
    for plant in user_plants:
        for note in plant.care_notes:
            notes_for_each_plant[plant].append(note)

    return render_template("my_plants.html", form=form, plants=user_plants,
                           total_user_plants=len(user_plants),
                           available_plants=available_plants,
                           notes_for_each_plant=notes_for_each_plant, logout_form=logout_form, user_name=current_user.first_name)

@views.route('/edit_plant', methods=['GET', 'POST'])
@login_required
@regular_user_required
def edit_plant():
    logout_form = LogoutForm()
    plant_id = request.args.get("plant_id", type=int) or request.form.get("plant_id", type=int)
    plant = UserPlant.query.get_or_404(plant_id)

    if plant.user_id != current_user.user_id:
        logging.warning("IDOR attempt: user_id {current_user.user_id} attempted to access plant_id {plant_id} " \
        "owned by user_id {plant.user_id} from IP: {request.remote_addr}")
        flash("You are not authorised to access this", category="error")
        abort(403)
        # return redirect(url_for("views.my_plants"))

    form = EditUserPlantForm(obj=plant)
    form.selected_plant_id.choices = [(p.plant_id, p.plant_type) for p in Plant.query.all()]
    form.plant_id.data = plant.user_plant_id

    if form.validate_on_submit():
        plant.plant_name = form.plant_name.data
        plant.last_watered = form.last_watered.data
        # calculation set to 7 days from when last watered
        plant.next_watering_date = plant.last_watered + timedelta(days=7)
        plant.plant_id = form.selected_plant_id.data

        if form.care_note.data:
            new_note = CareNote(
                user_plant_id=plant.user_plant_id,
                care_note=form.care_note.data,
                note_date=datetime.now(timezone.utc).date()
            )
            db.session.add(new_note)

        db.session.commit()
        flash(f"{plant.plant_name} updated successfully", category="success")
        return redirect(url_for("views.my_plants"))

    return render_template("edit_plant.html", form=form, plant=plant, logout_form=logout_form, user_name=current_user.first_name)

@views.route('/admin_base', methods=['GET'])
@login_required
@admin_required
def admin_base():
    logout_form = LogoutForm()
    users = User.query.all()
    total_users = User.query.count()
    total_user_plants = UserPlant.query.count()
    total_plants = Plant.query.count()

    plant_type_frequency = (
        db.session.query(Plant.plant_type, func.count(UserPlant.user_plant_id).label("count"))
        .outerjoin(UserPlant, Plant.plant_id == UserPlant.plant_id)
        .group_by(Plant.plant_type)
        .order_by(func.count(UserPlant.user_plant_id).desc())
        .all()
    )
    # most popular plant calculated after ordering
    if plant_type_frequency:
        most_popular_plant = plant_type_frequency[0][0]
    else:
        print("no plants")

    return render_template("admin_base.html", user=current_user, users=users, total_users=total_users, total_plants=total_plants, total_user_plants=total_user_plants, plant_type_frequency=plant_type_frequency, most_popular_plant=most_popular_plant, logout_form=logout_form, user_name=current_user.first_name)


# user home page
@views.route('/user_base')
@login_required
@regular_user_required
def user_base():
    logout_form = LogoutForm()
    return render_template("user_base.html", logout_form=logout_form, user_name=current_user.first_name)

@views.route('/plant_library', methods=['GET'])
@login_required
@regular_user_required
def plant_library():
    logout_form = LogoutForm()
    plants = Plant.query.all()
    return render_template("plant_library.html", user=current_user, plants=plants, logout_form=logout_form, user_name=current_user.first_name)


@views.route('/manage_library', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_library():
    logout_form = LogoutForm()
    plants = Plant.query.all()
    form = PlantLibraryForm()

    if form.validate_on_submit():
        new_plant = Plant(
            plant_type=form.plant_type.data,
            water=form.water.data,
            light=form.light.data,
            soil=form.soil.data
        )
        db.session.add(new_plant)
        db.session.commit()

        flash(f'{new_plant.plant_type} added to the plant library', category='success')
        return redirect(url_for("views.manage_library"))

    # invalid form submitted
    elif form.is_submitted():
        for field_errors in form.errors.values():
            for error in field_errors:
                flash(error, category="error")

    return render_template("manage_library.html", user=current_user, plants=plants, form=form, logout_form=logout_form, user_name=current_user.first_name)



@views.route('/edit_plant_library', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_plant_library():
    logout_form = LogoutForm()
    plant_id = request.args.get("plant_id", type=int) or request.form.get("plant_id", type=int)

    if not plant_id:
        flash("no plant ID provided", category='error')
        return redirect(url_for("views.manage_library"))

    plant = Plant.query.get_or_404(plant_id)
    # prefilled form info
    form = PlantLibraryForm(obj=plant)

    if form.validate_on_submit():
        plant.plant_type = form.plant_type.data
        plant.water = form.water.data
        plant.light = form.light.data
        plant.soil = form.soil.data

        db.session.commit()
        flash(f"{plant.plant_type} updated successfully!", category="success")
        return redirect(url_for("views.manage_library"))

    elif form.is_submitted():
        for field_errors in form.errors.values():
            for error in field_errors:
                flash(error, category='error')

    return render_template("edit_plant_library.html", plant=plant, form=form, logout_form=logout_form, user_name=current_user.first_name)


@views.route('/delete_plant', methods=['POST'])
@login_required
@admin_required
def delete_plant():
    form = DeletePlantForm()

    if form.validate_on_submit():
        plant_id = form.plant_id.data
        plant = Plant.query.get_or_404(plant_id)

        db.session.delete(plant)
        db.session.commit()
        flash(f"'{plant.plant_type}' deleted successfully!", category="success")
    else:
        flash("Invalid deletion request", category="error")

    return redirect(url_for("views.manage_library"))



