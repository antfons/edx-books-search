class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Book:
    def __init__(self, title, author, pub_year, isbn):
        self.title = title
        self.author = author
        self.pub_year = pub_year
        self.isbn = isbn

class Review:
    def __init__(self, text, rating, user_id, book_id):
        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.book_id = book_id