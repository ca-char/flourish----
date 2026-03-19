Flourish is a Flask-based plant care tracker web app

## Key features:

- User authentication: login, logout, register
- Role-based: admin and regular users
- CRUD functionality: view, add, edit and delete plants
- Care notes: add and view care notes for each plant
- Admin dashboard: user statistics and manage plant library

## Installation

- clone the repo: git clone https://github.com/ca-char/flourish----.git
- create a virtual environment:
  python3 -m venv venv  
  source venv/bin/activate (Linux/macOS)  
  venv\Scripts\activate (Windows)
- install dependencies by running pip install -r requirements.txt
- ensure the config.py file LOAD_SAMPLE_DATA = True for first time use and **init**.py create_db(reset=False). For preserving data: config.py file set create_db(reset=False), LOAD_SAMPLE_DATA = False
- run the application run.py

## Configuration

Create a .env file or set the environment variables

- FLASK_APP=web_app
- FLASK_ENV=development
- SECRET_KEY=your_secret_key
- DATABASE_URI=sqlite:///database.db

## Using the app

Once the server is running:

- Visit http://localhost:5000 in your browser
- Register a new account or log in as an existing user
  - Admin user: 'admin1@email.com', 'Admin1!'
  - Regular user: 'bob@email.com', 'Bobiscool1!'

Add your plants, enjoy!

- Find remaining user credentials for testing in sample_data.json

## Running Tests

- To run the test suite: pytest

## Hosted publicly
