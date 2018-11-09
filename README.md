# SendIT-challenge-2
Is a parcel delivery service app 

<!-- [![Build Status](https://travis-ci.com/dxania/Store_Manager_APIs.svg?branch=develop)](https://travis-ci.com/dxania/Store_Manager_APIs)
[![Coverage Status](https://coveralls.io/repos/github/dxania/Store_Manager_APIs/badge.svg?branch=develop)](https://coveralls.io/github/dxania/Store_Manager_APIs?branch=develop)
[![Code Climate](https://codeclimate.com/github/codeclimate/codeclimate/badges/gpa.svg)](https://codeclimate.com/github/dxania/Store_Manager_APIs) -->


## Features
The Program offers the following endpoints:


  | REQUEST           | ROUTE                      | FUNCTIONALITY                                      |
  |-------------------|----------------------------|----------------------------------------------------|
  |  GET              | /parcels                   | Fetch all parcel delivery orders                   |
  |  GET              | /parcels/[parcelId]        | Fetch a specific parcel delivery order             |                     
  |  GET              | /users/[userId]/parcels    | Fetch all parcel delivery orders by a specific user|                  
  |  PUT              | /parcels/[parcelId]/cancel | Cancel a specific parcel delivery order            | 
  |  POST             | /parcels                   | Create a parcel delivery order                     | 



## Getting started
These instructions will get you a copy of the program on your local machine for development and testing purposes. The instructions are tailored for uses of `LINUX OS` particularly `UBUNTU`

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