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

    response = requests.get(f"https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{make}?format=json")
    cars = response.json().get('Results')
    if not any(car['Model_Name'].lower() == model.lower() for car in cars):
        return jsonify({'ERROR': 'Car does not exist'}), 404

    new_car = Car(make=make, model=model)
    db.session.add(new_car)
    db.session.commit()

    return jsonify({'SUCCESS': 'Car was added to the database'}), 201

if __name__ == '__main__':
    app.run(debug=True)
