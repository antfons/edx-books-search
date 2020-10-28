# Project 1

Web Programming with Python and JavaScript 

The application uses 3 environment variables listed below: 

#Please set those variables below to use the application correctly
SET FLASK_APP=application.py \
SET DATABASE_URL= "your url" \
SET GOODREADS_KEY= "your key" 

Here are some steps that were recorded while the project has been developed: 

(X) Create user table \
(X) Create book table \
(X) Create review table \
(X) Check database connection \
(X) Import data from csv file \
(X) Insert User for testing \
(X) Studied about hashpassword using native hashlib library \
(X) Create password with sha512 for storage \
(X) Check user's correct password with sha512 \
(X) Create database manager for user methods \
(X) Create database manager for book methods 

(X) Search for books by isbn, title or author. used LIKE condition on all of them \
(X) Insert review \
(X) Get review from that the user made on a book \
(X) Get all reviews from a book \
(X) Get data from goodreads api  \
(X) Integrate data from goodreads with the app \
(X) Validade login creation \
(X) Validade review from same user \
(X) Apply CSS using bootstrap 

Project's structure: \
folder static/css containing css styles \
folder templates containing all the pages used on the project \
folder tests some tests files were made while developing the project 


Flask part: \
file: hash_pass.py contains the implemenation for user password using sha512 using the native lib hashlib. \
file: models.py contains the classes used on the project( User, Book and Review), for this one was not used orm. \
file: import.py file used to fill the database used on the project that is on heroku platform. \
file: application.py contains all the routes created to match the project's definition.
