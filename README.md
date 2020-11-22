# RecommenderonAWS

## Overview

This project is to provide both user based recommendation to the user using Flask, which is deployed on AWS EC2 instance. 
The database used in this project is Mysql and the recommendation system used are nearest neighbour.

## Structure

- src

    The source code for back end and database management.

- static

    The dependencies of javascript and css files for this project
    
- templates

    The front end files

- app

    The main execution file
    
- database

    The database file for this project
    
- requirements

    All the dependencies for this project
    
- settings

    Database settings

## Installation

- Environment

    Ubuntu 18.04, Windows 10, Python 3.5+

- Dependency Installation

    Please go ahead to this project repository and run the following command in terminal.
    
    ```
    pip3 install -r requirements.txt
    ```

- Database Installation

    Please setup mysql on your system and after creating database, import database.sql into your database.

## Execution

- Please set the database setting variables (DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST) in settings file.

- Please run the following command in the this project directory in terminal.

    ```
    python3 app.py
    ``` 
