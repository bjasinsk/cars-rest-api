import requests
from app import app, db
from car import Car

# cleaning the database before testing
with app.app_context():
    Car.query.delete()
    db.session.commit()


def test_add_car():
    """Test of adding a car to the database."""

    url = 'http://127.0.0.1:8000/cars'
    headers = {'Content-Type': 'application/json'}
    data = {'make': 'Toyota', 'model': 'Corolla'}
    response = requests.post(url, json=data, headers=headers)
    assert response.status_code == 201

def test_rate_car():
    """Test to add auto rating."""

    url = 'http://127.0.0.1:8000/rate'
    headers = {'Content-Type': 'application/json'}
    data = {'make': 'Toyota', 'model': 'Corolla', 'rating': 5}
    response = requests.post(url, json=data, headers=headers)
    assert response.status_code == 200

def test_add_the_same_car_rejection():
    """Test of adding second same car to database."""

    url = 'http://127.0.0.1:8000/cars'
    headers = {'Content-Type': 'application/json'}
    data = {'make': 'Toyota', 'model': 'Corolla'}
    response = requests.post(url, json=data, headers=headers)
    assert response.status_code == 400


def test_get_all_cars():
    """Download test of the list of all cars."""

    # cleaning the database before test
    with app.app_context():
        Car.query.delete()
        db.session.commit()

    add_car_data = [
        {'make': 'Toyota', 'model': 'Corolla'},
        {'make': 'Honda', 'model': 'Civic'},
        {'make': 'Honda', 'model': 'Accord'}
    ]
    url_add_car = 'http://127.0.0.1:8000/cars'
    for car in add_car_data:
        requests.post(url_add_car, json=car, headers={'Content-Type': 'application/json'})

    url = 'http://127.0.0.1:8000/cars'
    response = requests.get(url)
    assert response.status_code == 200
    assert len(response.json()) == len(add_car_data)


def test_get_popular_cars():
    """Download test of the list of the most popular cars."""

    # cleaning the database before test
    with app.app_context():
        Car.query.delete()
        db.session.commit()

    add_car_data = [
        {'make': 'Toyota', 'model': 'Corolla'},
        {'make': 'Honda', 'model': 'Civic'},
        {'make': 'Honda', 'model': 'Accord'}
    ]
    rate_data = [
        {'make': 'Honda', 'model': 'Accord', 'rating': 4},
        {'make': 'Honda', 'model': 'Accord', 'rating': 5},
        {'make': 'Honda', 'model': 'Accord', 'rating': 4},
        {'make': 'Honda', 'model': 'Civic', 'rating': 1},
        {'make': 'Toyota', 'model': 'Corolla', 'rating': 2},
        {'make': 'Honda', 'model': 'Civic', 'rating': 2}
    ]
    url_add_car = 'http://127.0.0.1:8000/cars'
    url_rate_car = 'http://127.0.0.1:8000/rate'
    for car in add_car_data:
        requests.post(url_add_car, json=car, headers={'Content-Type': 'application/json'})
    for rate in rate_data:
        requests.post(url_rate_car, json=rate, headers={'Content-Type': 'application/json'})

    response = requests.get('http://127.0.0.1:8000/popular')
    assert response.status_code == 200
    results = response.json()
    assert results[0]['model'] == 'Accord'
    assert results[1]['model'] == 'Civic'


def test_sort_by_make_when_same_votes():
    """Test that cars are sorted alphabetically by make when they have the same number of votes."""

    # cleaning the database before test
    with app.app_context():
        Car.query.delete()
        db.session.commit()

    cars_to_add = [
        {'make': 'Audi', 'model': 'A4', 'rating': 4},
        {'make': 'BMW', 'model': '320', 'rating': 4}
    ]

    for car in cars_to_add:
        requests.post('http://127.0.0.1:8000/cars', json={'make': car['make'], 'model': car['model']}, headers={'Content-Type': 'application/json'})
        requests.post('http://127.0.0.1:8000/rate', json={'make': car['make'], 'model': car['model'], 'rating': car['rating']}, headers={'Content-Type': 'application/json'})

    response = requests.get('http://127.0.0.1:8000/popular')
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) > 0
    assert response_data[0]['make'] == 'Audi'

def test_sort_by_model_when_same_make_and_votes():
    """Test that cars are sorted alphabetically by model when they have the same make and number of votes."""

    # cleaning the database before test
    with app.app_context():
        Car.query.delete()
        db.session.commit()

    cars_to_add = [
        {'make': 'Honda', 'model': 'Accord', 'rating': 5},
        {'make': 'Honda', 'model': 'Civic', 'rating': 5}
    ]

    for car in cars_to_add:
        requests.post('http://127.0.0.1:8000/cars', json={'make': car['make'], 'model': car['model']}, headers={'Content-Type': 'application/json'})
        requests.post('http://127.0.0.1:8000/rate', json={'make': car['make'], 'model': car['model'], 'rating': car['rating']}, headers={'Content-Type': 'application/json'})

    response = requests.get('http://127.0.0.1:8000/popular')
    sorted_cars = response.json()
    assert sorted_cars[0]['model'] == 'Accord' and sorted_cars[1]['model'] == 'Civic'

