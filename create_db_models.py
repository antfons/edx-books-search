import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Book(db.Model):
    __table_args__ = {'schema': 'project1'}
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    pub_year = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.String, nullable=False)


class User(db.Model):
    __table_args__ = {'schema': 'project1'}
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)


class Review(db.Model):
    __table_args__ = {'schema': 'project1'}
    __tablename__ = "review"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('project1.user.id'))
    fk_book_id = db.Column(db.Integer, db.ForeignKey('project1.book.id'))
    user = db.relationship("User")
    book = db.relationship("Book")



def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()