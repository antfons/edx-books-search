

# Edx Books Search 

![Backend lang](https://img.shields.io/badge/python-3.6-green)


![Gif](https://media.giphy.com/media/Y1w3UooFM7tnDpIn6k/giphy.gif)

[Youtube](https://www.youtube.com/watch?v=iliQXR3SIqc&t=48s "video")

#### Description
This project aims to create a books review website where users are able to make registration and log using username and a password. On this project users are able to search for books, give reviews for books and see reviews made by other users. On this project is also used data from an API provided by Goodreads to pull ratings. This projects uses server side rendering only.

## Table of content

- [**Getting Started**](#getting-started)
- [Built With](#built-with)
- [License](#license)
- [Motivation](#motivation)

## Getting Started
You can run this application by cloning the repository and running it with python.

### Requirements
- Python
- pipenv
- To use the application correctly, you'll also need a uri of your database. I've tested it with a postgres database hosted on heroku. [Heroku](https://www.heroku.com/ "Heroku")
- And you'll also need a public key for Goodreads API. [Goodreads](https://www.goodreads.com/api "Goodreads")

### Install python dependencies
```console
pipenv shell
```

### Set environment variables
```console
FLASK_APP=application.py
DATABASE_URL= URI of your sql database
GOODREADS_KEY= "your key"
```

### Usage
Before starting the flask app, ensure that you have a schema named 'project1' on your database, otherwise you'll have to change the database name on the code because it wasn't used any orm to perform the queries.


### Creating the tables
```console
python create_db_models.py
```

### Filling up the database: This script reads a csv file with 5000 rows with books data and insert on it, if you're not using a localhost database this step can take a long time to finish.
```console
python import.py
```
### Running the flask application

```console
flask run
```
### Open the application on the browser, create your user and start using it.

http://localhost:5000/

## Built With

### [Flask](https://flask.palletsprojects.com/en/1.1.x/ "Flask")
A lightweight WSGI web application framework for Python.
### Python
### HTML
### CSS
### [Bootstrap](https://getbootstrap.com/ "Bootstrap")

## License

This project is licensed under the [MIT License](https://github.com/antfons/edx-books-search/blob/main/LICENSE)


## Motivation
I've made this project while learning web development with Python and JavaScript and it's part of EDX HarvardX CS50's Web Programming with Python and JavaScript. [Edx Web Programming](https://courses.edx.org/courses/course-v1:HarvardX+CS50W+Web/course/ "Edx Web Programming")
