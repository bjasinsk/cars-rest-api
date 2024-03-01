import sys
import os
os.environ['TESTING'] = '1'

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import requests
from src.car import Car
from src.app import app, db


# Global variables
BASE_URL = 'http://127.0.0.1:8000'
CAR_URL = f'{BASE_URL}/cars'
RATE_URL = f'{BASE_URL}/rate'
POPULAR_URL = f'{BASE_URL}/popular'
HEADERS = {'Content-Type': 'application/json'}

# cleaning the database before testing
with app.app_context():
    Car.query.delete()
    db.session.commit()


def test_add_car():
    """
    Test of adding a car to the database.
    """
    data = {'make': 'Toyota', 'model': 'Corolla'}
    response = requests.post(CAR_URL, json=data, headers=HEADERS)
    assert response.status_code == 201


def test_rate_car():
    """
    Test to add auto rating.
    """
    data = {'make': 'Toyota', 'model': 'Corolla', 'rating': 5}
    response = requests.post(RATE_URL, json=data, headers=HEADERS)
    assert response.status_code == 200


def test_add_the_same_car_rejection():
    """
    Test of adding second same car to database.
    """
    data = {'make': 'Toyota', 'model': 'Corolla'}
    response = requests.post(CAR_URL, json=data, headers=HEADERS)
    assert response.status_code == 400


def test_get_all_cars():
    """
    Download test of the list of all cars.
    """

    # cleaning the database before test
    with app.app_context():
        Car.query.delete()
        db.session.commit()

    add_car_data = [{'make': 'Toyota', 'model': 'Corolla'}, {'make': 'Honda', 'model': 'Civic'},
                    {'make': 'Honda', 'model': 'Accord'}]
    for car in add_car_data:
        requests.post(CAR_URL, json=car, headers=HEADERS)
    response = requests.get(CAR_URL)
    assert response.status_code == 200
    assert len(response.json()) == len(add_car_data)


def test_get_popular_cars():
    """
    Download test of the list of the most popular cars.
    """

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
    for car in add_car_data:
        requests.post(CAR_URL, json=car, headers=HEADERS)
    for rate in rate_data:
        requests.post(RATE_URL, json=rate, headers=HEADERS)
    response = requests.get(POPULAR_URL)
    assert response.status_code == 200
    results = response.json()
    assert results[0]['model'] == 'Accord'
    assert results[1]['model'] == 'Civic'


def test_sort_by_make_when_same_votes():
    """
    Test that cars are sorted alphabetically by make when they have the same number of votes.
    """
    # cleaning the database before test
    with app.app_context():
        Car.query.delete()
        db.session.commit()

    cars_to_add = [
        {'make': 'Audi', 'model': 'A4', 'rating': 4},
        {'make': 'BMW', 'model': '320', 'rating': 4}
    ]

    for car in cars_to_add:
        requests.post(CAR_URL, json={'make': car['make'], 'model': car['model']}, headers=HEADERS)
        requests.post(RATE_URL, json={'make': car['make'], 'model': car['model'], 'rating': car['rating']},
                      headers=HEADERS)

    response = requests.get(POPULAR_URL)
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) > 0
    assert response_data[0]['make'] == 'Audi'


def test_sort_by_model_when_same_make_and_votes():
    """
    Test that cars are sorted alphabetically by model when they have the same make and number of votes.
    """
    # cleaning the database before test
    with app.app_context():
        Car.query.delete()
        db.session.commit()

    cars_to_add = [
        {'make': 'Honda', 'model': 'Accord', 'rating': 5},
        {'make': 'Honda', 'model': 'Civic', 'rating': 5}
    ]

    for car in cars_to_add:
        requests.post(CAR_URL, json={'make': car['make'], 'model': car['model']}, headers=HEADERS)
        requests.post(RATE_URL, json={'make': car['make'], 'model': car['model'], 'rating': car['rating']},
                      headers=HEADERS)

    response = requests.get(POPULAR_URL)
    sorted_cars = response.json()
    assert sorted_cars[0]['model'] == 'Accord' and sorted_cars[1]['model'] == 'Civic'
