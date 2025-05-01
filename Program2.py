#Program Written By: Ainsley Bellamy
#Date Written: 04/29/2025
#Program Title: Phonebook_Database


import sqlite3

#Initiate variables for CRUD operations; also while-loop control variable and minimum and maximum
#numbers that the user can enter.
MIN = 1
MAX = 5
CREATE = 1
READ = 2
UPDATE = 3
DELETE = 4
QUIT = 5

def main():
#This function initially creates the database file and populates it.
    create_populate_database()

#Control variable for while-loop;
#this while-loop continually checks for the user answer until they select 5 for quit.
    keep_going = 0
    while keep_going != 5:

#Call function to get user choice for CRUD operations or quit.
        keep_going = get_choice()

#Check what user's choice is by checking the updated keep_going variable from the get_choice() function.
        if keep_going == CREATE:
            create_new()
        elif keep_going == READ:
            read_row()
        elif keep_going == UPDATE:
            update_selection()
        elif keep_going == DELETE:
            delete_selection()

def create_populate_database():
#Create database.
    conn = sqlite3.connect('phonebook.db')

#Create cursor.
    cur = conn.cursor()

#Insert table.
    cur.execute('''DROP TABLE IF EXISTS Entries''')
    cur.execute('''CREATE TABLE Entries (ID INTEGER PRIMARY KEY NOT NULL, Names TEXT, Numbers TEXT)''')
#Insert fictional names and numbers.
    insertInfo(cur)

#Commit Changes.
    conn.commit()
#Close database file.
    conn.close()

#This is the function called to populate the database with fictional info.
def insertInfo(cur):
    contacts = [
        ("Luke Skywalker", "555-1122"),
        ("Leia Organa", "555-2233"),
        ("Han Solo", "555-3344"),
        ("Chewbacca", "555-4455"),
        ("Obi-Wan Kenobi", "555-5566"),
        ("Darth Vader", "555-6677"),
        ("Yoda", "555-7788"),
        ("R2-D2", "555-8899"),
        ("C-3PO", "555-9900"),
        ("Lando Calrissian", "555-1001")
    ]
    for row in contacts:
        cur.execute('''INSERT INTO Entries (Names, Numbers) VALUES (?,?)''', (row[0], row[1]))

#This function displays the menu to the user and assigns their choice to the variable keep_going.
#This function also returns keep_going with its new value.
def get_choice():
#First display choices.
    print("Enter The Number Of Your Choice From The Menu:")
    print("1. Create New Entry\n"
          "2. Search For Entry\n"
          "3. Update Entry\n"
          "4. Delete Entry\n"
          "5. Quit")
#Now allow the user to enter a number.
    try:
        keep_going = int(input(">>> "))
        while keep_going < MIN or keep_going > MAX or keep_going is None:
            print("You Can Select Options 1-5.")
            keep_going = int(input(">>> "))
        print(f"You Selected Option {keep_going}.")
        print()
        return keep_going
    except ValueError as err:
        print("Answer Can Only Be A Number; Answer Cannot Be Empty")
        print()

#These next few functions perform the CRUD operations.

#This function allows the user to add a new row to the phonebook database.
def create_new():
#First open the database and create cursor.
    try:
        conn = sqlite3.connect('phonebook.db')
        cur = conn.cursor()
#Get new name and number from user.
        name = input(str("Enter name for new entry: "))
        number = input(str(f"Enter number for {name}: "))
#Create new row and commit changes.
        cur.execute('''INSERT INTO Entries (Names, Numbers) VALUES (?,?)''', (name, number))
        conn.commit()
        print("Phonebook Updated")
        print()
    except sqlite3.Error as err:
        print("Error While Processing")
        print(err)
        print()
    except Exception as err:
        print(f"Error\n{err}")
        print()
    finally:
        conn.close()

#This function allows the user to search for a row name; it then displays all that it finds.
def read_row():
    try:
#Open database and get cursor.
        conn = sqlite3.connect('phonebook.db')
        cur = conn.cursor()
#Get user search.
        search = str(input("Enter A Name To Search For: "))
        cur.execute('''SELECT * FROM Entries WHERE lower(Names) == ?''', (search.lower(),))
        results = cur.fetchall()
        print(f"Found: {len(results)} Results")
        print("ID   Name                             Number")
        print("---------------------------------------------")
#Display all results.
        for row in results:
            print(f'{row[0]:<5}{row[1]:<30}{row[2]:>10}')
        print()
    except sqlite3.Error as err:
        print("Error While Searching")
        print(err)
        print()
    except Exception as err:
        print(f"Error\n{err}")
        print()
    finally:
        conn.close()

#This function allows the user to update a row of their choice.
def update_selection():
#First open database and create cursor.
    try:
        conn = sqlite3.connect('phonebook.db')
        cur = conn.cursor()
#Get which selection the user wants to update.
        search = int(input("Enter The Entry ID Number Of The Entry You Would Like To Update: "))
        cur.execute('''SELECT ID, Names, Numbers FROM Entries WHERE ID == ?''', (search,))
        results = cur.fetchone()
        if results != None:
            print(f"The Current Name And Number for Entry Number {search} is: "
                  f"{results[1]}, {results[2]}.")
#Get new info from user.
        name = str(input("Enter Updated Name: "))
        number = str(input("Enter Updated Number: "))
#Update with new info.
        cur.execute('''UPDATE Entries SET Names = ?, Numbers = ? WHERE ID == ?''', (name, number, search))
        conn.commit()
        print(f"Entry Number {search} Was Updated.")
        print()
    except sqlite3.Error as err:
        print("Error While Processing")
        print(err)
        print()
    except Exception as err:
        print(f"Error\n{err}")
        print()
    finally:
        if conn != None:
              conn.close()

#This function allows the reader to search for and delete a row.
def delete_selection():
    try:
#First open database and create cursor.
        conn = sqlite3.connect('phonebook.db')
        cur = conn.cursor()
#Allow the user to search for which row they want to delete.
        search = int(input("Enter The Product ID Number Of The Entry You Would Like To Delete: "))
        cur.execute('''SELECT ID, Names, Numbers FROM Entries WHERE ID == ?''', (search,))
        results = cur.fetchone()
        if results != None:
#Double check user selection.
            print(f"Are You Sure You Want To Delete This Entry? --- ID: {search}, "
                                f"Name: {results[1]}, Numbers: {results[2]}.")
            answer = str(input('Enter "y" for yes and "n" for no: '))
            if answer.lower() == 'y':
#Delete from database.
                cur.execute('''DELETE FROM Entries WHERE ID == ? AND Names == ? AND Numbers == ?''', (search, results[1], results[2]))
                print("Entry Deleted.")
            else:
                print("Forgoing Deletion")
        conn.commit()
        print()
    except sqlite3.Error as err:
        print("Error While Processing")
        print(err)
        print()
    except Exception as err:
        print(f"Error\n{err}")
        print()
    finally:
        if conn != None:
              conn.close()

#This is a function I created while writing the program which helped me keep track of what info was where.
#I have simply commented it out to save it for future use.
# def display():
#     conn = sqlite3.connect('phonebook.db')
#     cur = conn.cursor()
#     cur.execute('''SELECT * FROM Entries''')
#     results = cur.fetchall()
#     for row in results:
#         print(f'{row[0]:<5}{row[1]:<30}{row[2]:>10}')
#     print()

if __name__ == '__main__':
    main()