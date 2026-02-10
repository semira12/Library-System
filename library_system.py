import json
import os
from datetime import datetime, timedelta

FILE_NAME = "library_data.json"


class Book:
    def __init__(self, book_id, title, author, edition, year, status="Available", borrower="None", due_date=None,
                 waitlist=None):
        self.id = book_id
        self.title = title
        self.author = author
        self.edition = edition
        self.year = year
        self.status = status
        self.borrower = borrower
        self.due_date = due_date  # Format: YYYY-MM-DD
        self.waitlist = waitlist if waitlist else []

    def to_dict(self):
        return self.__dict__


class LibrarySystem:
    def __init__(self):
        self.books = []
        self.load_from_file()

    def load_from_file(self):
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, 'r') as f:
                data = json.load(f)
                self.books = [Book(**b) for b in data]

    def save_to_file(self):
        with open(FILE_NAME, 'w') as f:
            json.dump([b.to_dict() for b in self.books], f, indent=4)

    def add_book(self):
        print("\n--- Add New Book ---")
        try:
            book_id = int(input("Enter 4-digit Book ID: "))
            if any(b.id == book_id for b in self.books):
                print("Error: ID already exists!")
                return

            title = input("Enter Title: ")
            author = input("Enter Author: ")
            edition = int(input("Enter Edition: "))
            year = int(input("Enter Year: "))

            new_book = Book(book_id, title, author, edition, year)
            self.books.append(new_book)
            self.save_to_file()
            print("Book added successfully!")
        except ValueError:
            print("Invalid input. Please enter numbers for ID, Edition, and Year.")

    def display_inventory(self):
        if not self.books:
            print("Library is empty.")
            return
        print("\n" + "=" * 50)
        for b in self.books:
            print(f"ID: {b.id} | {b.title} by {b.author}")
            print(f"   Status: {b.status} | Due: {b.due_date}")
            if b.waitlist:
                print(f"   Waitlist: {len(b.waitlist)} person(s)")
            print("-" * 50)

    def search_and_borrow(self):
        query = input("Enter Title or Author to search: ").lower()
        matches = [b for b in self.books if query in b.title.lower() or query in b.author.lower()]

        if not matches:
            print("No matches found.")
            return

        for b in matches:
            print(f"ID: {b.id} | {b.title} ({b.status})")

        try:
            target_id = int(input("\nEnter ID to borrow (0 to cancel): "))
            if target_id == 0: return

            book = next((b for b in matches if b.id == target_id), None)
            if not book:
                print("Invalid ID.")
                return

            if book.status == "Issued":
                choice = input("Book is issued. Join waitlist? (y/n): ")
                if choice.lower() == 'y':
                    name = input("Enter your name: ")
                    book.waitlist.append(name)
                    self.save_to_file()
                    print(f"Added to waitlist. Position: {len(book.waitlist)}")
                return

            student = input("Enter Student Name: ")
            # Check if student already has a book
            if any(b.borrower == student for b in self.books):
                print(f"ALERT: {student} already has a borrowed book!")
                return

            # Calculate due date (7 days from now)
            due = datetime.now() + timedelta(days=7)
            book.status = "Issued"
            book.borrower = student
            book.due_date = due.strftime("%Y-%m-%d")

            self.save_to_file()
            print(f"Book issued! Due date: {book.due_date}")
        except ValueError:
            print("Invalid input.")

    def return_book(self):
        try:
            book_id = int(input("Enter Book ID to return: "))
            book = next((b for b in self.books if b.id == book_id), None)

            if not book or book.status == "Available":
                print("Book not found or not issued.")
                return

            # Simple Fine Calculation
            due_dt = datetime.strptime(book.due_date, "%Y-%m-%d")
            today = datetime.now()
            if today > due_dt:
                days_over = (today - due_dt).days
                print(f"OVERDUE! Days: {days_over} | Fine: ${days_over * 5}")
            else:
                print("Returned on time. No fine.")

            # Check Waitlist
            if book.waitlist:
                next_user = book.waitlist.pop(0)
                book.borrower = next_user
                book.due_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
                print(f"Notice: Auto-assigned to waitlist member: {next_user}")
            else:
                book.status = "Available"
                book.borrower = "None"
                book.due_date = None

            self.save_to_file()
        except ValueError:
            print("Invalid ID.")


def main():
    lib = LibrarySystem()
    menu = {
        "1": lib.add_book,
        "2": lib.display_inventory,
        "3": lib.search_and_borrow,
        "4": lib.return_book,
        "0": exit
    }

    while True:
        print("\n--- PYTHON LIBRARY SYSTEM ---")
        print("1. Add Book\n2. Display Inventory\n3. Search & Borrow\n4. Return Book\n0. Exit")
        choice = input("Choice: ")
        action = menu.get(choice)
        if action:
            if choice == "0": print("Exiting..."); break
            action()
        else:
            print("Invalid selection.")


if __name__ == "__main__":
    main()