# cars-rest-api

Repository intended for the project which is a simple REST API - a basic database of car makes and models working with an external API.

Project requires python version 3.10. Project runs locally on port 8000.

# 1. Launching the project

**Creation of an environment:**

$python -m venv venv

**Running the environment on a Unix-type system:**

$source venv/bin/activate

**Running the environment on Windows:**

$venv\Scripts\activate

**Installing the required libraries:**

$pip install -r requirements.txt

**To start the project using gunicorn:**

$gunicorn app:app

# 2. Run tests

To run the tests, go to the src subfolder in the terminal and then run the command:  

$pytest

# 3. How to test individually

Add a new car:  
$curl -X POST -H "Content-Type: application/json" -d '{"make": "Toyota", "model": "Corolla"}' http://127.0.0.1:8000/cars

Rate a car:  
$curl -X POST -H "Content-Type: application/json" -d '{"make": "Toyota", "model": "Corolla", "rating": 5}' http://127.0.0.1:8000/rate

Get all cars:  
$curl -X GET http://127.0.0.1:8000/cars

Get popular cars:  
$curl -X GET http://127.0.0.1:8000/popular

# 4. Models
The car class represents an auto in the database, it has fields in it such as:
-id - an identifier to pass in the database 
- make - the brand name of the car
- model - the name of the car model
- avarage_rate - the average rating the car has received at a given time
- vote_count - the number of votes with a rating on this car 

# 5. Endpoints
**POST /cars**  
Description: Add a new car to the database.
Request body: JSON object with make and model.   
Response: JSON object indicating success or failure.

**POST /rate**  
Description: Submit a rating for a car.
Request body: JSON object with make, model, and rating.  
Response: JSON object indicating success or failure.

**GET /cars**  
Description: Retrieve a list of all cars.  
Response: JSON array of cars with details.  

**GET /popular**  
Description: Retrieve a list of cars sorted by popularity (number of votes) and alphabetically by make and model if necessary.  
Response: JSON array of popular cars with details.
