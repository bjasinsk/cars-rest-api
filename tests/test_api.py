import requests
from app import app, db
from car import Car

# cleaning the database before testing
with app.app_context():
    Car.query.delete()
    db.session.commit()


def test_add_car():
    url = 'http://127.0.0.1:8000/cars'
    headers = {'Content-Type': 'application/json'}
    data = {'make': 'Toyota', 'model': 'Corolla'}
    response = requests.post(url, json=data, headers=headers)
    assert response.status_code == 201

def test_rate_car():
    url = 'http://127.0.0.1:8000/rate'
    headers = {'Content-Type': 'application/json'}
    data = {'make': 'Toyota', 'model': 'Corolla', 'rating': 5}
    response = requests.post(url, json=data, headers=headers)
    assert response.status_code == 200

def test_add_the_same_car_rejection():
    url = 'http://127.0.0.1:8000/cars'
    headers = {'Content-Type': 'application/json'}
    data = {'make': 'Toyota', 'model': 'Corolla'}
    response = requests.post(url, json=data, headers=headers)
    assert response.status_code == 400