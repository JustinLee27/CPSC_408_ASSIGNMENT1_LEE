# Justin Lee
# 2371816
# justlee@chapman.edu
# CPSC 408-01
# Assignment 1
import random
import sqlite3
import csv

# Create a database in sqlite called StudentDB and a table called Student
conn = sqlite3.connect('./StudentDB.db')
mycursor = conn.cursor()

# Create a list of faculty advisors
advisors = ["Dr. Stevens", "Dr. Linstead", "Dr. German", "Dr. Joe", "Dr. Shmoe"]

# Check if the "Students" table already exists
mycursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Students'")
table_exists = mycursor.fetchone()

if not table_exists:
    # The "Students" table doesn't exist, so create it
    mycursor.execute("CREATE TABLE Students (StudentID INTEGER PRIMARY KEY, FirstName TEXT, LastName TEXT, GPA REAL, Major TEXT, FacultyAdvisor TEXT, Address TEXT, City TEXT, State TEXT, ZipCode TEXT, MobilePhoneNumber TEXT, isDeleted INTEGER);")
    conn.commit()
    print("Table 'Students' created.")
else:
    print("Table 'Students' already exists.")

# Function to import the data from student.csv into the database
def import_data():
    # Read the CSV file and insert its contents into the database
    with (open('./students.csv', 'r') as csvfile):
        reader = csv.DictReader(csvfile)
        for row in reader:
            sql = "INSERT INTO Students (FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber, isDeleted) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            val = (
                row["FirstName"],
                row["LastName"],
                row["GPA"],
                row["Major"],
                random.choice(advisors),
                row["Address"],
                row["City"],
                row["State"],
                row["ZipCode"],
                row["MobilePhoneNumber"],
                0
            )
            mycursor.execute(sql, val)
            conn.commit()


import_data()

# Function to display all students
def display_all_students():
    mycursor.execute("SELECT * FROM Students WHERE isDeleted = 0")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)


# Function to add a new student
def add_student():
    # Get the student's information
    while True:
        firstName = input("Enter the student's first name: ")
        if firstName.isalpha() and len(firstName) > 0:
            break
        else:
            print("Invalid input. Please enter a valid first name.\n")

    while True:
        lastName = input("Enter the student's last name: ")
        if lastName.isalpha() and len(lastName) > 0:
            break
        else:
            print("Invalid input. Please enter a valid last name.")

    while True:
        try:
            gpa = float(input("Enter the student's GPA: "))
            if 0.0 <= gpa <= 4.0:
                break
            else:
                print("Invalid input. GPA must be between 0.0 and 4.0.")
        except ValueError:
            print("Invalid input. GPA must be a numeric value.")

    while True:
        major = input("Enter the student's major: ")
        if len(major) > 0:
            break
        else:
            print("Invalid input. Please enter a valid major.")

    while True:
        facultyAdvisor = input("Enter the student's faculty advisor: ")
        if len(facultyAdvisor) > 0:
            break
        else:
            print("Invalid input. Please enter a valid faculty advisor.")

    while True:
        address = input("Enter the student's address: ")
        if len(address) > 0:
            break
        else:
            print("Invalid input. Please enter a valid address.")

    while True:
        city = input("Enter the student's city: ")
        if len(city) > 0:
            break
        else:
            print("Invalid input. Please enter a valid city.")

    while True:
        state = input("Enter the student's state: ")
        if len(state) > 0 and state.isalpha():
            break
        else:
            print("Invalid input. Please enter a valid state.")

    while True:
        zipCode = input("Enter the student's zip code: ")
        if zipCode.isnumeric() and len(zipCode) == 5:
            break
        else:
            print("Invalid input. Zip code must be a 5-digit numeric value.")

    while True:
        mobilePhoneNumber = input("Enter the student's mobile phone number: ")
        if mobilePhoneNumber.isnumeric() and len(mobilePhoneNumber) == 10:
            break
        else:
            print("Invalid input. Mobile phone number must be a 10-digit numeric value.")

    # Insert the student into the database
    sql = "INSERT INTO Students (FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber, isDeleted) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    val = (
        firstName,
        lastName,
        gpa,
        major,
        facultyAdvisor,
        address,
        city,
        state,
        zipCode,
        mobilePhoneNumber,
        0
    )
    mycursor.execute(sql, val)
    conn.commit()

    print("Student added successfully.")


# Function to update a student
def update_student():
    # Get the student's ID
    while True:
        try:
            studentID = int(input("Enter the student's ID: "))
            break
        except ValueError:
            print("Invalid input. Student ID must be a numeric value.")

    # Check if the student exists
    mycursor.execute("SELECT * FROM Students WHERE StudentID = ? AND isDeleted = 0", (studentID,))
    myresult = mycursor.fetchone()
    if myresult:
        # The student exists, so update their information
        while True:
            major = input("Enter the student's major: ")
            if len(major) > 0:
                break
            else:
                print("Invalid input. Please enter a valid major.")

        while True:
            facultyAdvisor = input("Enter the student's faculty advisor: ")
            if len(facultyAdvisor) > 0:
                break
            else:
                print("Invalid input. Please enter a valid faculty advisor.")

        while True:
            phoneNumber = input("Enter the student's mobile phone number: ")
            if phoneNumber.isnumeric() and len(phoneNumber) == 10:
                break
            else:
                print("Invalid input. Mobile phone number must be a 10-digit numeric value.")

        # Update the student's information in the database
        sql = "UPDATE Students SET Major = ?, FacultyAdvisor = ?, MobilePhoneNumber = ? WHERE StudentID = ?"
        val = (major, facultyAdvisor, phoneNumber, studentID)
        mycursor.execute(sql, val)
        conn.commit()


# Function to delete a student
def delete_student():
    # Get the student's ID
    while True:
        try:
            studentID = int(input("Enter the student's ID who you wish to delete: "))
            break
        except ValueError:
            print("Invalid input. Student ID must be a numeric value.")

    # Check if the student exists
    mycursor.execute("SELECT * FROM Students WHERE StudentID = ? AND isDeleted = 0", (studentID,))
    myresult = mycursor.fetchone()
    if myresult:
        # The student exists, so delete them from the database
        sql = "UPDATE Students SET isDeleted = 1 WHERE StudentID = ?"
        val = (studentID,)
        mycursor.execute(sql, val)
        conn.commit()
        print("Student deleted successfully.")
    else:
        print("Student not found.")


# Function to search for a student by major, GPA, state, city, or faculty advisor
def search_student():
    print("\nSearch Menu:")
    print("1. Search by Major")
    print("2. Search by GPA")
    print("3. Search by State")
    print("4. Search by City")
    print("5. Search by Faculty Advisor")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        search_by_major()
    elif choice == "2":
        search_by_gpa()
    elif choice == "3":
        search_by_state()
    elif choice == "4":
        search_by_city()
    elif choice == "5":
        search_by_faculty_advisor()
    elif choice == "6":
        print("Exiting the search menu.")
    else:
        print("Invalid choice. Please select a valid option.")


# Function to search for a student by major
def search_by_major():
    # Get the major
    while True:
        major = input("Enter the student's major: ")
        if len(major) > 0:
            break
        else:
            print("Invalid input. Please enter a valid major.")

    # Search for the student by major
    mycursor.execute("SELECT * FROM Students WHERE Major = ? AND isDeleted = 0", (major,))
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)


# Function to search for a student by GPA
def search_by_gpa():
    # Get the GPA
    while True:
        try:
            gpa = float(input("Enter the student's GPA: "))
            if 0.0 <= gpa <= 4.0:
                break
            else:
                print("Invalid input. GPA must be between 0.0 and 4.0.")
        except ValueError:
            print("Invalid input. GPA must be a numeric value.")

    # Search for the student by GPA
    mycursor.execute("SELECT * FROM Students WHERE GPA = ? AND isDeleted = 0", (gpa,))
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)


# Function to search for a student by state
def search_by_state():
    # Get the state
    while True:
        state = input("Enter the student's state: ")
        if len(state) > 0 and state.isalpha():
            break
        else:
            print("Invalid input. Please enter a valid state.")

    # Search for the student by state
    mycursor.execute("SELECT * FROM Students WHERE State = ? AND isDeleted = 0", (state,))
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)


# Function to search for a student by city
def search_by_city():
    # Get the city
    while True:
        city = input("Enter the student's city: ")
        if len(city) > 0:
            break
        else:
            print("Invalid input. Please enter a valid city.")

    # Search for the student by city
    mycursor.execute("SELECT * FROM Students WHERE City = ? AND isDeleted = 0", (city,))
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)


# Function to search for a student by faculty advisor
def search_by_faculty_advisor():
    # Get the faculty advisor
    while True:
        facultyAdvisor = input("Enter the student's faculty advisor: ")
        if len(facultyAdvisor) > 0:
            break
        else:
            print("Invalid input. Please enter a valid faculty advisor.")

    # Search for the student by faculty advisor
    mycursor.execute("SELECT * FROM Students WHERE FacultyAdvisor = ? AND isDeleted = 0", (facultyAdvisor,))
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)


# Main program loop
def main():
    while True:
        print("Database Initialized.")
        print("\nMenu:")
        print("1. Display All Students")
        print("2. Add New Student")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Search for Student")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            display_all_students()
        elif choice == "2":
            add_student()
        elif choice == "3":
            update_student()
        elif choice == "4":
            delete_student()
        elif choice == "5":
            search_student()
        elif choice == "6":
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please select a valid option.")


main()
