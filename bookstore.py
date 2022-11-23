# We import sqlite3
import sqlite3

# We declare a boolean variable for our while loop later
is_book_keeping = True

# We declare our database under db variable(this connects to the file that we either already have
# or if not, then it creates the file
db = sqlite3.connect('data/ebookstore_db')

# We create a cursor object that is used to execute SQL statements
cursor = db.cursor()

# We create a list of tuples with information about the books in the table
book_list =[(3001, "A Tale of Two Cities", 'Charles Dickens', 30),
               (3002, "Harry Potter and the Philosopher's Stone",'J.K. Rowling', 40),
               (3003, "The Lion, the Witch and the Wardrobe",'C.S. Lewis', 25),
               (3004, "The Lord of the Rings",'J.R.R. Tolkien', 37),
               (3005, "Alice in Wonderland", 'Lewis Caroll', 12)]

# We use a try and except method in case the table is already in the system
# In this case We have anticipated this and we just inform the user that the table already exists
# When we try to create the same table.
# We execute a command to create a table with 4 columns, id, Title, Author and Qty
# id is labeled an int and the primary key, the Title  and Author as text and Qty as an integer
# We then exceute the command with db.commit()
try:
    cursor.execute('''
         CREATE TABLE books(id INTEGER PRIMARY KEY, Title TEXT, Author TEXT, QTY INTEGER)
    ''')
    db.commit()
except sqlite3.OperationalError:
    print("The table has already been created")

try:
    cursor.executemany ('''INSERT INTO books(id, Title, Author, Qty) VALUES(?,?,?,?)''',
    book_list)

except sqlite3.IntegrityError:
    print("The data from the last have already been inserted in the table")


# We define a function enter_book
# The function asks the user to input the details of a book in this case
# the id, author, title and qty. We use a try and except method.
# Because of the list of information we are looking for,we ask that the user
# enter the information accurately.  We use the except exception to tell the user
# to enter information accurately(when we catch any error) if any of the details are not properly typed in.
# We use the INSERT INTO command to insert the book details in our database
# if all the information has been accepted by the system.
# We also use a while loop to allow the user to reenter details if something went wrong.
def enter_book():
    is_entering = True
    while is_entering:
        try:
            print("Add the details of the book you want to enter into the system")
            add_id = int(input("Enter book id: "))
            add_title = input("Enter book title: ")
            add_author = input("Enter book author: ")
            add_qty = int(input("Enter stock quantity of the book: "))
            cursor.execute('''INSERT INTO books(id, Title, Author, Qty)
            VALUES(?,?,?,?)''',(add_id, add_title, add_author, add_qty,))
            db.commit()
            print("\nBook Successfully Added\n")
            is_entering = False
        except exception:
            print("Please make sure you have enter the respective information correctly.")


# This function allows the user to enter an id number (as it is the primary key)
# to find a book that needs updating. We make a while loop to allow user to keep trying if
# something went wrong.  We ask the user to choose what details of the selected book needs changing.
# The menu options might be in numbers, but we keep them as a string so as to avoid having the ValueError.
# We use the UPDATE and SET commands to change the values according to the user and execute with db.commit()
def update_book():
    is_updating = True
    while is_updating:
        try:
            book_id = int(input("Enter the id numberof the book you'd like to update:\n"))
        except ValueError:
            print("Enter a valid id number")
            continue

        cursor.execute('''SELECT * from books WHERE id = ?''',(book_id,))
        selected_book = cursor.fetchone()
        print(f"""Book Found!
id:{selected_book[0]}, Title: {selected_book[1]}, 
Author: {selected_book[2]}, Qty: {selected_book[3]}\n""")

        update_choice = input('''What about the book would you like to update:
1 - id
2 - Title
3- Author
4 - Qty
5- Cancel
''')
        if update_choice == "1":
            new_id = int(input("Enter the new id numberfor the book?: "))
            cursor.execute('''UPDATE books SET id = ? WHERE id = ?''',
                           (new_id, book_id))
            db.commit()
            print("\nUpdate has been Successful\n")
            is_updating = False

        elif update_choice == "2":
            new_title = input("Enter the updated title for the book: ")
            cursor.execute('''UPDATE books SET Title = ? WHERE id = ?''',
                           (new_title, book_id))
            db.commit()
            print("\nUpdate has been Successful\n")
            is_updating = False

        elif update_choice == "3":
            new_author = input("Enter the updated author for the book: ")
            cursor.execute('''UPDATE books SET Author = ? WHERE id = ?''',
                           (new_author, book_id))
            db.commit()
            print("\nUpdate has been Successful\n")
            is_updating = False

        elif update_choice == "4":
            new_qty = int(input("Enter the updated quantity for the book: "))
            cursor.execute('''UPDATE books SET Qty = ? WHERE id = ?''',
                           (new_qty, book_id))
            db.commit()
            print("\nUpdate has been Successful\n")
            is_updating = False

        elif update_choice == "5":
            is_updating = False

        else:
            print("Choice not found.  Please select from the choices above.")


# Similar to the above, as the id is the primary key, we ask user to enter the id of the book
# they want to delete.  We show them the book selected and ask them to confirm
# We use the delete command and execute with db.commit()
# We print a message to confirm deletion
def delete_book():
    book_id = int(input("Enter the id numberof the book you'd like to update:\n"))
    cursor.execute('''SELECT * from books WHERE id = ?''',(book_id,))
    selected_book = cursor.fetchone()
    print(f"""Delete this book?
id:{selected_book[0]}, Title: {selected_book[1]}, 
Author: {selected_book[2]}, Qty: {selected_book[3]}\n""")
    delete_confirmation = input("Enter y to delete book and enter any to leave as is: ").lower()
    if delete_confirmation == "y":
        cursor.execute('''DELETE FROM books WHERE id = ?''', (book_id,))
        db.commit()
        print(f"\nThe book with id number {book_id} has been deleted from the system.\n")


    else:
        print("Book has not been deleted from the system")


# We define a function search book that allows a user to search book by id, author and title
# We have also incorporated a search all function to show all books from the database
# Because of the amount of information we are asking from the user and ensure
# continuity of use, we have used except exception to capture any errors and allow the user to
# try again. For this reason we have used all if on the conditionals and not elifs as the syntax would now allow
# elifs as we try to capture any error entered. We use the SELECT command and use WHERE to set the conditions and find
# a specific book/books.
def search_book():
    is_searching = True
    while is_searching:
        try:
            search_choice = input("""Seach a book by
(Enter the number of your choice):
1 - id
2- Title
3 - Author
4 - Search all
5 - Back to main menu
""")

            print("""Please make sure you enter the details acurrately, an incorrect entry
will bring you back to the main menu""")
            try:
                if search_choice == "1":
                    searched_book_id = int(input("""Enter the id number of the book you're looking for:\n"""))
                    cursor.execute('''SELECT * from books WHERE id = ?''', (searched_book_id,))
                    selected_book = cursor.fetchone()
                    print(f"""Book Found!
id:{selected_book[0]}, Title: {selected_book[1]}, 
Author: {selected_book[2]}, Qty: {selected_book[3]}\n""")
                is_searching = False

                if search_choice == "2":
                    searched_book_title = input("Enter the Title of the book you're looking for:\n")
                    searched_books = cursor.execute('''SELECT * from books WHERE Title = ?''', (searched_book_title,))
                    for id, title, author, qty in searched_books:
                        print(f"""Book Found!
id: {id}, Title: {title}, 
Author: {author}, Qty: {qty}\n""")
                is_searching = False

                if search_choice == "3":
                    searched_book_author = input("Enter the Author of the book you're looking for:\n")
                    searched_books = cursor.execute('''SELECT * from books WHERE Author = ?''', (searched_book_author,))
                    for id, title, author, qty in searched_books:
                        print(f"""Book Found!
id: {id}, Title: {title}, 
Author: {author}, Qty: {qty}\n""")
                is_searching = False

                if search_choice == "4":
                    searched_books = cursor.execute('''SELECT * from books''')
                    print("Search results:")
                    for id, title, author, qty in searched_books:
                        print(f"""
id: {id}, Title: {title}, 
Author: {author}, Qty: {qty}""")
                is_searching = False

                if search_choice == "5":
                    is_searching = False

                else:
                    print("Please enter a valid option.  Try again.")

            except Exception:
                print("Please make sure you've entered the details correctly.")

        except ValueError:
            print("Please enter a valid number from the options")

# This is our main while loop.  We print a menu and we allow a user to select from the options.
# We use conditionals to call the functions according to the choice of the user.  We capture
# any invalid input with an else statement. We kept the numbers as strings to avoid having any
# ValueError is the user enters a letter or different character
while is_book_keeping:
    try:
        menu = input("""What would you like to do:
1 - Enter Book(Enter a new book in the database)
2 - Update Book(Update details about a certain book
3 - Delete a book
4 - Search for a book in the database
5 - Exit
""")

        if menu == "1":
            enter_book()
        elif menu == "2":
            update_book()
        elif menu == "3":
            delete_book()
        elif menu == "4":
            search_book()
        elif menu == 2:
            exit()
        else:
            print("Please choose a valid option from above.")

    except ValueError:
        ("Please enter a valid number from the menu.")