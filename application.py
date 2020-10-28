import os
import sys
sys.path.append(".")
import json
from flask import Flask, session, render_template, request, url_for, redirect
from flask_session import Session
from database_manager import DatabaseManager
from models import User, Review
from hash_pass import HashablePassword
app = Flask(__name__,static_folder='./static')

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
db_manager = DatabaseManager()
hash_obj = HashablePassword()

@app.route("/", methods=["GET"])
def index():
    if session:
        return render_template("search.html", title="Search Page")
    return render_template("index.html", title="EDX Project1")


@app.route("/", methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User(
            username,
            password
        )
        user_exist = db_manager.user_exists(user)
        if not user_exist:
            response_message = "Invalid user"
            return render_template("index.html", db_result=response_message)
        else:
            user_db = db_manager.get_user_by_name(user)
            password_is_correct = hash_obj.compare_hash(
                user_db.password,
                user.password
            )
            if password_is_correct:
                session["user_id"] = user_db.id
                session["username"] = user_db.username
                return render_template("search.html", title="Search Page")
            else:
                return render_template("index.html", db_result="Invalid password", title="EDX Project1")

    return render_template("index.html", db_result="Invalid user", title="EDX Project1")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return render_template("index.html", title="EDX Project1")


@app.route("/signup", methods=["POST"])
def signup():
    return render_template("signup.html", title="User creation")


@app.route("/dosignup", methods=["POST"])
def dosignup():
    username = request.form.get("username")
    password = request.form.get("password")
    user = User(
        username,
        password
    )
    user_exists = db_manager.user_exists(user)
    if user_exists:
        response_message = f"Username {user.username} exists, please choose another"
        return render_template("signup.html", db_result=response_message, title="User creation")
    user.password = hash_obj.create_hash_password(password)
    db_manager.insert_user(user)
    response_message = f"User {user.username} created, you can login now"
    return render_template("index.html", db_result=response_message, title="User creation")


@app.route("/search_books", methods=["POST"])
def search_books():
    information = request.form.get("information")
    books_list = db_manager.search_book(information)
    if books_list:
        return render_template("books_list.html", books=books_list, title="Book List")
    db_message = "Not match was found for your search"
    return render_template("search.html", title="Book Page", db_result=db_message)
    

@app.route("/search_books/<int:book_id>", methods=["GET"])
def more_information(book_id):
    book = db_manager.get_book_by_id(book_id)
    book_response = {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "year": book.pub_year,
        "isbn": book.isbn    
    }
    goodread_response = db_manager.get_book_from_goodreads(book.isbn)
    if goodread_response:
        book_response["review_count"] = goodread_response["books"][0]["work_ratings_count"] 
        book_response["average_rating"] = goodread_response["books"][0]["average_rating"]
    reviews = db_manager.get_all_reviews_by_book_id(book_id)
    return render_template("book_details.html", book=book_response, reviews=reviews, title="Book Review")


@app.route("/insert_review", methods=["POST"])
def insert_review():
    user_id = session["user_id"]
    book_id = request.form.get("book_id")
    review_text = request.form.get("review_text")
    review_rating = request.form.get("rating")
    review = Review(
        review_text,
        review_rating,
        user_id,
        book_id
    )
    review_db = db_manager.get_review_by_book_and_user_id(book_id, user_id)
    if not review_db:
        try:
            db_manager.insert_review(review)
            return redirect(url_for('more_information', book_id = book_id))
        except Exception:
            return redirect(url_for('more_information', book_id = book_id))

    db_result = "You cannot review the same book twice"
    book = db_manager.get_book_by_id(book_id)
    book_response = {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "year": book.pub_year,
        "isbn": book.isbn    
    }
    goodread_response = db_manager.get_book_from_goodreads(book.isbn)
    if goodread_response:
        book_response["review_count"] = goodread_response["books"][0]["work_ratings_count"] 
        book_response["average_rating"] = goodread_response["books"][0]["average_rating"]
    reviews = db_manager.get_all_reviews_by_book_id(book_id)
    return render_template("book_details.html", book=book_response, reviews=reviews, title="Book Review", db_result=db_result)

        
@app.route("/api/<string:isbn>")
def get_by_isbn(isbn):
    book = db_manager.search_book(isbn)
    book = book[0]
    book_response = {
        "title": book.title,
        "author": book.author,
        "year": book.pub_year,
        "isbn": book.isbn
    }
    if book:
        goodread_response = db_manager.get_book_from_goodreads(isbn)
        if goodread_response:
            book_response["review_count"] = goodread_response["books"][0]["work_ratings_count"] 
            book_response["average_rating"] = goodread_response["books"][0]["average_rating"]
    return json.dumps(book_response)