[![Build Status](https://travis-ci.org/wasibani-roy/SendIT-challenge-2.svg?branch=feature-make-parcel-order-%23161834974)](https://travis-ci.org/wasibani-roy/SendIT-challenge-2)[![Coverage Status](https://coveralls.io/repos/github/wasibani-roy/SendIT-challenge-2/badge.svg?branch=feature-make-parcel-order-%23161834974)](https://coveralls.io/github/wasibani-roy/SendIT-challenge-2?branch=feature-make-parcel-order-%23161834974)[![Maintainability](https://api.codeclimate.com/v1/badges/2c1a80866d94de0dc9ed/maintainability)](https://codeclimate.com/github/wasibani-roy/SendIT-challenge-2/maintainability)
# SendIT-challenge-2
Is a parcel delivery service app

## Features
The Program offers the following endpoints:


  | REQUEST           | ROUTE                      | FUNCTIONALITY                                      |
  |-------------------|----------------------------|----------------------------------------------------|
  |  GET              | /parcels                   | Fetch all parcel delivery orders                   |
  |  GET              | /parcels/[parcelId]        | Fetch a specific parcel delivery order             |                     
  |  GET              | /users/[userId]/parcels    | Fetch all parcel delivery orders by a specific user|                  
  |  PUT              | /parcels/[parcelId]/cancel | Cancel a specific parcel delivery order            | 
  |  POST             | /parcels                   | Create a parcel delivery order                     | 


## Prerequisites
What things you will need to run the application

```
Python3
    version: 3.6
```
```
Flask to build the application
```
```
Pytest to perform tests
```

## Installing
To have a copy of the project on your machine, run the command below in your preferred directory:

``` 
https://github.com/wasibani-roy/SendIT-challenge-2.git
```
After cloning, you will have a folder named `SendIT-challenge-2`


## Testing
Run pytest in the directory of the project to run tests


## Author
Roy
