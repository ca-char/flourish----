from web_app.models import User, Plant, UserPlant

def test_plant_model_creation():
    plant = Plant(plant_type="Monstera", water="Weekly", light="Bright", soil="Peaty")
    assert plant.plant_type == "Monstera"
    assert plant.water == "Weekly"
    assert plant.light == "Bright"
    assert plant.soil == "Peaty"


def test_user_plant_model_relationship():
    user = User(user_id=1, email="grower@example.com")
    plant = Plant(plant_id=2, plant_type="Cactus")
    user_plant = UserPlant(user_id=1, plant_id=2, plant_name="Spikey")
    assert user_plant.user_id == user.user_id
    assert user_plant.plant_id == plant.plant_id
    assert user_plant.plant_name == "Spikey"