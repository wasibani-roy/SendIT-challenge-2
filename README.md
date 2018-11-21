# SendIT-challenge-3

[![Build Status](https://travis-ci.org/wasibani-roy/SendIT-challenge-2.svg?branch=SendIT-api)](https://travis-ci.org/wasibani-roy/SendIT-challenge-2)
[![Coverage Status](https://coveralls.io/repos/github/wasibani-roy/SendIT-challenge-2/badge.svg?branch=SendIT-api)](https://coveralls.io/github/wasibani-roy/SendIT-challenge-2?branch=SendIT-api)
[![Maintainability](https://api.codeclimate.com/v1/badges/2c1a80866d94de0dc9ed/maintainability)](https://codeclimate.com/github/wasibani-roy/SendIT-challenge-2/maintainability)



## SendIT with Database

This application interacts with a PostgreSQL database to save user data and is meant for use parcel delivery service.

### Prerequisites

- You need to have Python3 installed on your computer. To install it go to [www.python.org](https://www.python.org/). Note: Python needs to be installed globally (not in the virtual environment)

### Features

- Usercan signin/signout from the application
- User can make a parcel delivery order
- User can view all orders they have made
- User can access a single order by its ID
- User can change destination of parcel

Additional features:

- Admin can view all orders made on the application
- Admin can change the present location and delivery status of parcel.

### Getting Started

Clone the project to your computer either by downloading the zip or using git. If you are downloading it then choose theStore-api branch and download that. To use git, run the code below:
```
    https://github.com/wasibani-roy/SendIT-challenge-2.git
```

Go into the folder, create a virtual environment, activate it and then use a pip command to install the requirements necessary for the app to function. Below are the steps to take:
```
   pip install -r requirements.txt
```
Next we need to set the Enviroment variable that is going to hold the database we want to 
use in our development enviroment
```
   set DATABASE_URL=sendit (For windows) or export DATABASE_URL=sendit(for Linux)
```
When this is done then run the application by typing this command
```
    python run.py
```



### Tests

To run tests, make sure that pytest or nose is installed. you can run that command to install them
```
    $ pip install -r requirements.txt
```
Next we need to set the Enviroment variable that is going to hold the database we want to 
use in our test enviroment
```
   set DATABASE_URL=sendit_test_db or export DATABASE_URL=sendit_test_db
```
Then run these commands to begin testing the API
```
    pytest
```

### Endpoints covered.

 HTTP Method | End point | Action | Access
-------|-------|-------|-------
 POST | /api/v2/auth/signup | Register a user  
 POST | /api/v2/auth/login | Login a user | 
 POST | /api/v2/parcels | Create a parcel order | only logged in User 
 GET | /api/v2/parcels/user/<parcel_id> | Get specific order by its ID | 
 PUT | /api/v2/parcels/<parcel_id>/destination | Change destination of parcel  
 GET | /api/v2/parcels/user | Fetch all products for a single user |  
 PUT | /api/v2/parcels/<parcel_id>/status | Admin change delivery status of a given order | 
 PUT | /api/v2/parcels/<parcel_id>/presentLocation | Admin cna change present location of parcel |  
 

### Built With
- [Python](https://www.python.org/)

### Authors

Wasibani Roy