# cars-rest-api

Repository intended for the project which is a simple REST API - a basic database of car makes and models working with an external API.

Project requires python version 3.10. Project runs locally on port 8000.

# The reason why there are two branches
The use of relative imports (such as from .car import db, Car) is recommended in cases where you are running the application in an environment that supports such a directory structure, Heroku being such an environment. However, when you run the application locally on your computer Python may not be able to resolve relative paths correctly, resulting in import errors. 
For this reason, I put the version of the project with relative paths on the main branch from which the version on Heroku is hosted.
On the other hand, I put the version with direct imports on the test-locally branch, so that I can run tests on it and test the application locally.

# 1. Launching the project

**Creation of an environment:**

$python -m venv venv

**Running the environment on a Unix-type system:**

$source venv/bin/activate

**Running the environment on Windows:**

$venv\Scripts\activate

**Installing the required libraries:**

$pip install -r requirements.txt

**To start the project using gunicorn run command in main folder**

$gunicorn --chdir src app:app

# 2. Run tests locally

To run the tests, go to the tests subfolder in the terminal and then run the command:  

$pytest


# 3. How to test rest api operations locally (version on test-locally branch)

Below are only examples of endpoints, adding and rating automobiles works for any car, just replace the data in the command:  

**Add a new car:**    
$curl -X POST -H "Content-Type: application/json" -d '{"make": "Toyota", "model": "Corolla"}' http://127.0.0.1:8000/cars

**Rate a car:**   
$curl -X POST -H "Content-Type: application/json" -d '{"make": "Toyota", "model": "Corolla", "rating": 5}' http://127.0.0.1:8000/rate

**Get all cars:**   
$curl -X GET http://127.0.0.1:8000/cars

**Get popular cars:**  
$curl -X GET http://127.0.0.1:8000/popular

# 4. How to test rest api operations on Heroku
Below are only examples of endpoints, adding and rating automobiles works for any car, just replace the data in the command:  

**Add a new car:**  
$curl -X POST -H "Content-Type: application/json" -d "{\"make\":\"Toyota\", \"model\":\"Yaris\"}" https://shrouded-citadel-19343-1561f1cd2280.herokuapp.com/cars

**Rate a car:**  
$curl -X POST -H "Content-Type: application/json" -d "{\"make\":\"Toyota\", \"model\":\"Corolla\", \"rating\":5}" https://shrouded-citadel-19343-1561f1cd2280.herokuapp.com/rate

**Get all cars:**  
$curl https://shrouded-citadel-19343-1561f1cd2280.herokuapp.com/cars

**Get popular cars:**  
$curl https://shrouded-citadel-19343-1561f1cd2280.herokuapp.com/popular


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


