import os

from models import *
from database_manager import DatabaseManager
import csv



def main():
    db_manager = DatabaseManager()
    fails_counter = 0
    added_count = 0
    
    with open("books.csv") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for isbn, title, author, pub_year in reader:
            book = Book(
                title,
                author,
                pub_year,
                isbn
            )
            book_db = db_manager.search_book(book.isbn)
            if not book_db:
                try:
                    db_manager.insert_book(book)
                    db_manager.commit()
                    added_count +=1
                except Exception as ex:
                    print(ex)
                    fails_counter+= 1
                    print(fails_counter)
                    pass
        print(f"Added: {added_count} books")
    
                

            
            

if __name__ == "__main__":
    main()
