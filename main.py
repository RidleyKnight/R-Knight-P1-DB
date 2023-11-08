
import sqlite3
import csv

conn = sqlite3.connect("StudentDB.db")
mycursor = conn.cursor()

mycursor.execute('''
    CREATE TABLE IF NOT EXISTS Student (
        StudentId INTEGER PRIMARY KEY,
        FirstName TEXT,
        LastName TEXT,
        GPA REAL,
        Major TEXT,
        FacultyAdvisor TEXT,
        Address TEXT,
        City TEXT,
        State TEXT,
        ZipCode TEXT,
        MobilePhoneNumber TEXT,
        isDeleted INTEGER
    )
''')



def displayMenu():
    print("Functions:")
    print("1: Import students.csv in to the database.")
    print("2: Display StudentsDB.")
    print("3: Enter Student.")
    print("4: Change Student Data.")
    print("5: Delete a Student.")
    print("6: Find Students.")
    print("7: Exit.")

def importData():
    try:
        with open('students.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for row in csv_reader:
                if len(row) == 9:
                    mycursor.execute('''
                       INSERT INTO Student (FirstName, LastName, GPA, Major, Address, City, State, ZipCode, MobilePhoneNumber)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                       ''', (row[0], row[1], float(row[8]), row[7], row[2], row[3], row[4], row[5], row[6]))
                else:
                    print("Row incomplete")
            print("Data Imported")
    except sqlite3.Error as e:
        print("Error importing data:", str(e))

def printDatabase():
    mycursor.execute("SELECT * FROM Student WHERE isDeleted IS NULL")
    rows = mycursor.fetchall()
    if len(rows) > 0:
        for row in rows:
            print(row)
    else:
        print("Database Empty")

def enterStudent():
    first_name = input("Enter First Name: ")
    if first_name.isdigit():
        print("Please enter a name without numbers")
        enterStudent()
        return
    if len(first_name) > 20:
        print("That's a very long first name but I won't judge")
    last_name = input("Enter Last Name: ")
    if last_name.isdigit():
        print("Please enter a name without numbers")
        enterStudent()
        return
    if len(last_name) > 20:
        print("That's a very long last name but I won't judge")
    address = input("Enter Address: ")
    city = input("Enter City: ")
    state = input("Enter State Abbreviation: ")
    if state.isdigit():
        print("Please enter a state without numbers")
        enterStudent()
        return
    if len(state) > 2:
        print("Please enter a state Abbreviation")
        enterStudent()
        return
    zip_code = input("Enter Zip Code: ")
    if len(zip_code) != 5:
        print("Please enter a valid zip code")
        enterStudent()
        return
    if zip_code.isalpha():
        print("Please enter a valid zip code")
        enterStudent()
        return
    phone_number = input("Enter Mobile Phone Number: ")
    if len(phone_number) != 10:
        print("Please enter a valid Phone number")
        enterStudent()
        return
    if phone_number.isalpha():
        print("Please enter a valid Phone number")
        enterStudent()
        return
    major = input("Enter Major: ")
    gpa = input("Enter GPA: ")
    if gpa.isalpha():
        print("Please enter a valid GPA")
        enterStudent()
        return
    gpa = float(gpa)
    if gpa < 0.0:
        print("Please enter a valid GPA, ")
        enterStudent()
        return
    if gpa > 5.0:
        print("Please enter a valid GPA")
        enterStudent()
        return

    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Student (FirstName, LastName, Address, City, State, ZipCode, MobilePhoneNumber, Major, GPA)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (first_name, last_name, address, city, state, zip_code, phone_number, major, gpa))
    conn.commit()
    print("Student Added")

def updateStudent(sID):
    if sID == 0:
        sID = input("Enter the ID of the Student you wish to edit: ")
    if sID != 0:
        print("Editable aspects:")
        print("1: Major")
        print("2: Advisor")
        print("3: Phone Number")
        print("4: Return To Menu")
        choice = input("Select an aspect to change: ")
        if choice == '1':
            newMajor = input("Enter the new Major: ")
            mycursor.execute(
                "UPDATE Student SET Major = ? WHERE StudentId = ?",
                (newMajor, sID))
        elif choice == '2':
            newAdvisor = input("Enter the new Advisor: ")
            mycursor.execute(
                "UPDATE Student SET FacultyAdvisor = ? WHERE StudentId = ?",
                (newAdvisor, sID))
        elif choice == '3':
            newPH = input("Enter the new Phone Number: ")
            if len(newPH) != 10:
                print("Please enter a valid Phone number")
                updateStudent(sID)
                return
            if newPH.isalpha():
                print("Please enter a valid Phone number")
                updateStudent(sID)
                return
            else:
                mycursor.execute(
                    "UPDATE Student SET MobilePhoneNumber = ? WHERE StudentId = ?",
                    (newPH, sID))
        elif choice == '4':
            return
        else:
            print("Please enter a valid option.")
            updateStudent(sID)

def annhilateStudent():
    sID = input("Enter Student ID for Termination: ")
    mycursor.execute("UPDATE Student SET isDeleted = 1 WHERE StudentId = ?", (sID,))
    conn.commit()

def searchStudents():
    print("Searchable aspects:")
    print("1: Major")
    print("2: GPA")
    print("3: City")
    print("4: State")
    print("5: Advisor")
    choice = input("Select an aspect to search by: ")
    if choice == '1':
        major = input("Enter a major: ")
        mycursor.execute("SELECT * FROM Student WHERE Major = ? AND isDeleted is null", (major,))
        rows = mycursor.fetchall()
        if len(rows) != 0:
            print(f"Students studying {major}:")
            for row in rows:
                print(row)
        else:
            print(f"{major} does not seem to have any students studying it")
    elif choice == '2':
        gpa = input("Enter a GPA: ")
        mycursor.execute("SELECT * FROM Student WHERE GPA = ? AND isDeleted is null", (gpa,))
        rows = mycursor.fetchall()
        if len(rows) != 0:
            print(f"Students with a {gpa} GPA:")
            for row in rows:
                print(row)
        else:
            print(f"How strange, no one seems to have a gpa of {gpa}")
    elif choice == '3':
        city = input("Enter a city: ")
        mycursor.execute("SELECT * FROM Student WHERE City = ? AND isDeleted is null", (city,))
        rows = mycursor.fetchall()
        if len(rows) != 0:
            print(f"Students from {city}:")
            for row in rows:
                print(row)
        else:
            print(f"No students seem to live in {city}")
    elif choice == '4':
        state = input("Enter a state: ")
        mycursor.execute("SELECT * FROM Student WHERE State = ? AND isDeleted is null", (state,))
        rows = mycursor.fetchall()
        if len(rows) != 0:
            print(f"Students from {state}:")
            for row in rows:
                print(row)
        else:
            print(f"No students seem to live in {state}")
    elif choice == '5':
        advisor = input("Enter an advisor: ")
        mycursor.execute("SELECT * FROM Student WHERE Advisor = ? AND isDeleted is null", (advisor,))
        rows = mycursor.fetchall()
        if len(rows) != 0:
            print(f"Students with {advisor} as an advisor:")
            for row in rows:
                print(row)
        else:
            print(f"There are no students with {advisor} as an advisor")


while True:
    displayMenu()
    choice = input("Enter the number of an option above: ")

    if choice == '1':
        importData()
    elif choice == '2':
        printDatabase()
    elif choice == '3':
        enterStudent()
    elif choice == '4':
        updateStudent(0)
    elif choice == '5':
        annhilateStudent()
    elif choice == '6':
        searchStudents()
    elif choice == '7':
        print("SEVERING CONNECTION TO THE MAINFRAME!")
        mycursor.close()
        conn.close()
        break
    else:
        print("This does not seem to be an option. Please select a valid function.")


