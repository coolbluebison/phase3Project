The Arcane Library Management System
=====================================

The Arcane Library Management System is a simple halloween themed, Python-based program that helps manage and organize library operations. 

Through the use of SQLAlchemy, it interacts with a SQLite database to store and manage data related to books, students, and borrowing records.

## Modules

### 1. arcanelibrary.py

#### Overview:

This module is responsible for setting up the database, defining the schema and seeding for the library's operations. 

Establish a connection to the SQLite database.
- Define relationships between tables, e.g., a book can have many borrow records.
- Seeding: Intentionally commented out after the initial seeding. Delete the database and uncomment the lines to start over with sample data.


#### Tables:

- `Book`: Stores simple information about books, the title and author.
- `Student`: Stores simple information about students, their name and class year.
- `BorrowRecord`: Keeps track of the borrowing activities, indicating which student borrowed which book, and the relevant dates for borrowing and returning the book.


- 

### 2. cli.py

#### Overview:

This module provides a command-line interface (CLI) for users (librarians) to interact with the system.

#### Features:

- Welcome menu to start the operations.
- Choice menu to guide the user through available functionalities.
- Ability to:
  - View all books.
  - View all students.
  - Add new books or admit new students.
  - Record a borrowing or return a book.
  - View outstanding loans or the entire loan history.
  - Update book details.
  - Destroying a book 
  - Banning a student.

The CLI is also decorated with some artistic representations to give users a thematic feel of "The Arcane Library".

## Setup

1. Ensure Python is installed.
2. Install SQLAlchemy: `pip install sqlalchemy` or 'pipenv install'
3. Run `arcanelibrary.py` to set up the database.
4. (Optional) Uncomment the seeding section in `arcanelibrary.py` to populate your database with sample data.
5. Run `cli.py` to start the command-line interface and begin library management tasks.

## Usage

Runn `cli.py`. You will be greeted with the welcome menu. Press ENTER to proceed. The choice menu guides you through the possible actions. 

Type the number corresponding to your desired action and follow the on-screen instructions.

## Notes

- Students with borrowed books that have not been returned cannot be banned immediately. However, if you do decide to ban a student, the system will mark all their borrowings as returned.

---

Happy Halloween!!!