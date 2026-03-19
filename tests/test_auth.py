from flask import url_for
from web_app.models import User
from werkzeug.security import generate_password_hash

def test_login_page_loads(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Log in to Flourish" in response.data

def test_login_valid_user(client, app):
    with app.app_context():
        user = User(
            first_name='Bob',
            email='bob_test@email.com',
            password=generate_password_hash('Bobisnotcool!')
        )
        from web_app.extensions import db
        db.session.add(user)
        db.session.commit()

    response = client.post('/login', data={
        'email': 'bob_test@email.com',
        'password': 'Bobisnotcool!'
    }, follow_redirects=True)

    assert b'Flourish' in response.data
    assert response.status_code == 200

def test_login_invalid_user(client):
    response = client.post('/login', data={
        'email': 'invalid@example.com',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    assert b'Invalid email or incorrect password. Please try again.' in response.data

def test_logout(client, app):
    from web_app.models import User
    from web_app.extensions import db, bcrypt
    # from werkzeug.security import generate_password_hash


    with app.app_context():
        user = User(email='logout@example.com', password=bcrypt.generate_password_hash('logoutpass').decode('utf-8'), first_name='Out')
        db.session.add(user)
        db.session.commit()

    client.post('/login', data={'email': 'logout@example.com', 'password': 'logoutpass'}, follow_redirects=True)
    response = client.post('/logout', follow_redirects=True)
    assert b'Log in to Flourish' in response.data

def test_register_new_user(client, app):
    response = client.post('/register', data={
        'first_name': 'Harry',
        'email': 'harrypotter@example.com',
        'password1': 'ReallyStrongpasswordlol1!',
        'password2': 'ReallyStrongpasswordlol1!'
    }, follow_redirects=True)

    assert b'Create a new account' not in response.data
    assert b'Flourish' in response.data