from web_app import create_app

app = create_app({
    'TESTING': True,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    'WTF_CSRF_ENABLED': False,
})

if __name__ == '__main__':
    app.run(debug=True)
