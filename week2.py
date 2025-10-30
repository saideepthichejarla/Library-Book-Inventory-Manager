import json
import os
from typing import Dict, List, Optional

class Book:
    def __init__(self, isbn: str, title: str, author: str):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.issued_to: Optional[str] = None  
    
    def issue_to(self, user_id: str) -> bool:
        if self.issued_to is None:
            self.issued_to = user_id
            return True
        return False
    
    def return_book(self) -> bool:
        if self.issued_to is not None:
            self.issued_to = None
            return True
        return False
    
    def is_issued(self) -> bool:
        return self.issued_to is not None
    
    def to_dict(self) -> Dict:
        return {
            "isbn": self.isbn,
            "title": self.title,
            "author": self.author,
            "issued_to": self.issued_to
        }
    
    @classmethod
    def from_dict(cls, d: Dict):
        b = cls(d["isbn"], d["title"], d["author"])
        b.issued_to = d.get("issued_to")
        return b

class Library:
    def __init__(self, data_file: str = "library_data.json"):
        self.books_by_isbn: Dict[str, Book] = {}
        self.books_by_title: Dict[str, List[Book]] = {}
        self.books_by_author: Dict[str, List[Book]] = {}
        self.data_file = data_file
        self.load_data()
    
    def add_book(self, isbn: str, title: str, author: str) -> bool:
        if isbn in self.books_by_isbn:
            print(f"Book with ISBN {isbn} already exists.")
            return False
        book = Book(isbn, title, author)
        self.books_by_isbn[isbn] = book
        self.books_by_title.setdefault(title.lower(), []).append(book)
        self.books_by_author.setdefault(author.lower(), []).append(book)
        print(f"Added book: ISBN={isbn}, Title={title}, Author={author}")
        return True
    
    def search_by_title(self, title: str) -> List[Book]:
        return self.books_by_title.get(title.lower(), [])
    
    def search_by_author(self, author: str) -> List[Book]:
        return self.books_by_author.get(author.lower(), [])
    
    def issue_book(self, isbn: str, user_id: str) -> bool:
        book = self.books_by_isbn.get(isbn)
        if book is None:
            print(f"No book with ISBN {isbn} found.")
            return False
        if book.issue_to(user_id):
            print(f"Issued book ISBN={isbn} to user {user_id}")
            return True
        else:
            print(f"Book ISBN={isbn} is already issued to {book.issued_to}")
            return False
    
    def return_book(self, isbn: str) -> bool:
        book = self.books_by_isbn.get(isbn)
        if book is None:
            print(f"No book with ISBN {isbn} found.")
            return False
        if book.return_book():
            print(f"Book ISBN={isbn} has been returned.")
            return True
        else:
            print(f"Book ISBN={isbn} was not issued.")
            return False
    
    def total_books(self) -> int:
        return len(self.books_by_isbn)
    
    def issued_count(self) -> int:
        return sum(1 for b in self.books_by_isbn.values() if b.is_issued())
    
    def save_data(self):
        data = [b.to_dict() for b in self.books_by_isbn.values()]
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {self.data_file}")
    
    def load_data(self):
        if not os.path.isfile(self.data_file):
            print(f"No data file found at {self.data_file}. Starting fresh.")
            return
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            for d in data:
                book = Book.from_dict(d)
                self.books_by_isbn[book.isbn] = book
                self.books_by_title.setdefault(book.title.lower(), []).append(book)
                self.books_by_author.setdefault(book.author.lower(), []).append(book)
            print(f"Loaded {len(self.books_by_isbn)} books from {self.data_file}")
        except Exception as e:
            print(f"Error loading data from {self.data_file}: {e}")
    
    def report(self):
        print("=== Library Report ===")
        print(f"Total books: {self.total_books()}")
        print(f"Issued books: {self.issued_count()}")
        print(f"Available books: {self.total_books() - self.issued_count()}")
        print("======================")
        
def main():
    lib = Library()
    
    while True:
        print("\nLibrary Menu:")
        print("1. Add book")
        print("2. Search by title")
        print("3. Search by author")
        print("4. Issue book")
        print("5. Return book")
        print("6. Report")
        print("7. Save & Exit")
        choice = input("Enter choice (1-7): ").strip()
        
        if choice == "1":
            isbn = input("Enter ISBN: ").strip()
            title = input("Enter Title: ").strip()
            author = input("Enter Author: ").strip()
            lib.add_book(isbn, title, author)
        elif choice == "2":
            title = input("Enter Title to search: ").strip()
            results = lib.search_by_title(title)
            if results:
                print(f"Found {len(results)} book(s):")
                for b in results:
                    status = f"Issued to {b.issued_to}" if b.is_issued() else "Available"
                    print(f"  ISBN: {b.isbn}, Title: {b.title}, Author: {b.author}, Status: {status}")
            else:
                print("No books found by that title.")
        elif choice == "3":
            author = input("Enter Author to search: ").strip()
            results = lib.search_by_author(author)
            if results:
                print(f"Found {len(results)} book(s):")
                for b in results:
                    status = f"Issued to {b.issued_to}" if b.is_issued() else "Available"
                    print(f"  ISBN: {b.isbn}, Title: {b.title}, Author: {b.author}, Status: {status}")
            else:
                print("No books found by that author.")
        elif choice == "4":
            isbn = input("Enter ISBN to issue: ").strip()
            user_id = input("Enter User ID: ").strip()
            lib.issue_book(isbn, user_id)
        elif choice == "5":
            isbn = input("Enter ISBN to return: ").strip()
            lib.return_book(isbn)
        elif choice == "6":
            lib.report()
        elif choice == "7":
            lib.save_data()
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice — please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()