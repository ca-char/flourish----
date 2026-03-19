def test_add_user_plant(client, app):
    # need to be logged in
    from werkzeug.security import generate_password_hash
    from web_app.models import User, Plant
    from web_app.extensions import db

    with app.app_context():
        user = User(email='plantuser@example.com', password=generate_password_hash('testplant123'), first_name='Grower')
        plant = Plant(plant_type='Monstera', water='Weekly', light='Bright', soil='Peaty')
        db.session.add_all([user, plant])
        db.session.commit()

    client.post('/login', data={'email': 'plantuser@example.com', 'password': 'testplant123'}, follow_redirects=True)

    response = client.post('/my_plants', data={
        'plant_name': 'Leafy',
        'plant_id': 1,
        'last_watered': '2024-06-01',
        'care_note': 'Loves the sun.'
    }, follow_redirects=True)

    assert b'Leafy added successfully' in response.data