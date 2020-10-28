import os
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *


class DatabaseManager:
    def __init__(self):
        self.engine = create_engine(os.getenv("DATABASE_URL"))
        self.db = scoped_session(sessionmaker(bind=self.engine))

    def insert_book(self, book):
        self.db.execute("INSERT INTO project1.book (title, author, pub_year, isbn)\
            VALUES (:title, :author, :pub_year, :isbn)",
            {"title": book.title, "author": book.author,
             "pub_year": book.pub_year, "isbn": book.isbn
            })
        self.commit()


    def get_all_books(self):
        return self.db.execute("SELECT * FROM project1.book").fetchall()


    def get_book_by_id(self, id):
        return self.db.execute("SELECT * FROM project1.book WHERE id = :id",
        {"id": id}).fetchone()


    def search_book(self, information):
        isbn_books = self.db.execute("SELECT * FROM project1.book WHERE isbn like :isbn",
                {"isbn": f"%{information}%"}).fetchall()
        if isbn_books:
            return isbn_books

        title_books = self.db.execute("SELECT * FROM project1.book WHERE title like :title",
                {"title": f"%{information}%"}).fetchall()

        author_books = self.db.execute("SELECT * FROM project1.book WHERE author like :author",
                {"author": f"%{information}%"}).fetchall()       
        
        if title_books and author_books:
            return title_books + author_books
        elif title_books:
            return title_books
        elif author_books:
            return author_books
        return None            
        

    def commit(self):
        self.db.commit()

    
    def insert_user(self, user):
        try:
            self.db.execute("INSERT INTO project1.user (username, password)\
            VALUES (:username, :password)",
            {"username": user.username, "password": user.password})
            self.commit()
        except Exception as ex:
            print(ex)


    def get_user_by_name(self, user):
        try:
            db_user = self.db.execute("SELECT * FROM project1.user WHERE username = :username",
            {"username": user.username}).fetchone()
            if db_user is None:
                return None
            if db_user.username == user.username:
                return db_user
            return None
        except Exception as ex:
            print(ex)
            return None
            

    def user_exists(self, user):
        try:
            db_user = self.db.execute("SELECT * FROM project1.user WHERE username = :username",
            {"username": user.username}).fetchone()
            if db_user is None:
                return False
            if db_user.username == user.username:
                return True
            return False
        except Exception as ex:
            print(ex)
            return False

    def insert_review(self, review):
        reviews = self.db.execute("SELECT * FROM project1.review WHERE fk_book_id = :id",
        {"id" : review.book_id}).fetchall()
        if review.user_id in [r.user_id for r in reviews]:
            return None
        self.db.execute("INSERT INTO project1.review (text, rating, user_id, fk_book_id)\
            VALUES (:text, :rating, :user_id, :fk_book_id)",
            {"text": review.text, "rating": review.rating,
            "user_id": review.user_id, "fk_book_id": review.book_id})
        self.commit()
        return True

    def get_all_reviews(self):
        return self.db.execute("SELECT * FROM project1.review").fetchall()

    def get_all_reviews_by_book_id(self, book_id):
        return self.db.execute("SELECT review.id, text, rating, username FROM project1.review\
            JOIN project1.user ON project1.user.id = project1.review.user_id WHERE \
            review.fk_book_id = :book_id",
        {"book_id": book_id }).fetchall()

    def get_review_by_book_and_user_id(self, book_id, user_id):
        return self.db.execute("SELECT review.id, text, rating, username FROM project1.review\
            JOIN project1.user ON project1.user.id = project1.review.user_id WHERE review.user_id\
            = :user_id AND review.fk_book_id = :book_id",
        {"user_id": user_id, "book_id": book_id }).fetchone()

    def get_book_from_goodreads(self, isbn):
        res = requests.get("https://www.goodreads.com/book/review_counts.json",
        params={"key": os.getenv("GOODREADS_KEY"), "isbns": isbn})
        if res:
            return res.json()
        return None
        
