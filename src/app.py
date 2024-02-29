from flask import Flask, request, jsonify
from car import db, Car
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/cars', methods=['POST'])
def add_car():
    data = request.json
    make = data.get('make')
    model = data.get('model')

    existing_car = Car.query.filter_by(make=make, model=model).first()
    if existing_car:
        return jsonify({'ERROR': 'Car already exists'}), 400

    response = requests.get(f"https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{make}?format=json")
    cars = response.json().get('Results')
    if not any(car['Model_Name'].lower() == model.lower() for car in cars):
        return jsonify({'ERROR': 'Car does not exist'}), 404

    new_car = Car(make=make, model=model)
    db.session.add(new_car)
    db.session.commit()
    return jsonify({'SUCCESS': 'Car was added to the database'}), 201

@app.route('/rate', methods=['POST'])
def rate_car():
    data = request.json
    make = data.get('make')
    model = data.get('model')
    rating = data.get('rating')

    if make is None:
        return jsonify({'ERROR': 'Missing make'}), 400

    if model is None:
        return jsonify({'ERROR': 'Missing model'}), 400

    if rating is None:
        return jsonify({'ERROR': 'Missing rating'}), 400

    try:
        rating = int(rating)
    except ValueError:
        return jsonify({'ERROR': 'Rating must be an integer'}), 400

    if not (1 <= rating <= 5):
        return jsonify({'ERROR': 'Rating must be between 1 and 5'}), 400

    car = Car.query.filter_by(make=make, model=model).first()
    if car:
        total_rating = car.average_rate * car.vote_count + rating
        car.vote_count += 1
        car.average_rate = total_rating / car.vote_count
        db.session.commit()
        return jsonify({'SUCCESS': f'{make} {model} rated with {rating}'}), 200
    else:
        return jsonify({'ERROR': 'Car does not exist'}), 404

@app.route('/cars', methods=['GET'])
def get_cars():
    cars = Car.query.all()
    cars_list = []
    for car in cars:
        cars_list.append({
            'id': car.id,
            'make': car.make,
            'model': car.model,
            'average_rate': car.average_rate,
            'votes': car.vote_count
        })
    return jsonify(cars_list), 200

@app.route('/popular', methods=['GET'])
def get_popular_cars():
    cars = Car.query.order_by(Car.vote_count.desc()).all()
    popular_cars_list = []
    for car in cars:
        popular_cars_list.append({
            'id': car.id,
            'make': car.make,
            'model': car.model,
            'average_rate': car.average_rate,
            'votes': car.vote_count
        })
    return jsonify(popular_cars_list), 200


if __name__ == '__main__':
    app.run(debug=True)
