# cars-rest-api

Repository intended for the project which is a simple REST API - a basic database of car makes and models working with an external API.

Project requires python version 3.10. Project runs locally on port 8000.

# 1. Launching the project

**Creation of an environment:**

```bash
$python -m venv venv
```

**Running the environment on a Unix-type system:**

```bash
$source venv/bin/activate
```

**Running the environment on Windows:**

```bash
$venv\Scripts\activate
```

**Installing the required libraries:**

```bash
$pip install -r requirements.txt
```

**To start the project using gunicorn run command in main folder**

```bash
$gunicorn --chdir src app:app
```

# 2. Run tests locally

To run the tests, go to the tests subfolder in the terminal and then run the command:

```bash
$pytest
```

# 3. How to test rest api operations locally (version on test-locally branch)

Below are only examples of endpoints, adding and rating automobiles works for any car, just replace the data in the command:

**Add a new car:**

```bash
$curl -X POST -H "Content-Type: application/json" -d '{"make": "Toyota", "model": "Corolla"}' http://127.0.0.1:8000/cars
```

**Rate a car:**

```bash
$curl -X POST -H "Content-Type: application/json" -d '{"make": "Toyota", "model": "Corolla", "rating": 5}' http://127.0.0.1:8000/rate
```

**Get all cars:**

```bash
$curl -X GET http://127.0.0.1:8000/cars
```

**Get popular cars:**

```bash
$curl -X GET http://127.0.0.1:8000/popular
```

# 4. How to test rest api operations on Heroku

Below are only examples of endpoints, adding and rating automobiles works for any car, just replace the data in the command:

**Add a new car:**

```bash
$curl -X POST -H "Content-Type: application/json" -d "{\"make\":\"Toyota\", \"model\":\"Yaris\"}" https://shrouded-citadel-19343-1561f1cd2280.herokuapp.com/cars
```

**Rate a car:**

```bash
$curl -X POST -H "Content-Type: application/json" -d "{\"make\":\"Toyota\", \"model\":\"Corolla\", \"rating\":5}" https://shrouded-citadel-19343-1561f1cd2280.herokuapp.com/rate
```

**Get all cars:**

```bash
$curl https://shrouded-citadel-19343-1561f1cd2280.herokuapp.com/cars
```

**Get popular cars:**

```bash
$curl https://shrouded-citadel-19343-1561f1cd2280.herokuapp.com/popular
```

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
