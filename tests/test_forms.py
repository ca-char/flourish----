from web_app.forms import RegisterForm, AddUserPlantForm

def test_register_form_fields(app):
    with app.app_context():
        form = RegisterForm()
        assert hasattr(form, "email")
        assert hasattr(form, "first_name")
        assert hasattr(form, "password1")
        assert hasattr(form, "password2")

def test_add_user_plant_form_fields(app):
    with app.app_context():
        form = AddUserPlantForm()
        assert hasattr(form, "plant_name")
        assert hasattr(form, "plant_id")
        assert hasattr(form, "last_watered")
        assert hasattr(form, "care_note")