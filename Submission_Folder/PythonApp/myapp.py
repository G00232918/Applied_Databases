# Python App created by James Connolly
# Student Number - G00232918
# Applied Databases


# import to read SQL database
import pymysql

# get datetime
from datetime import datetime

# os used to write and create file
import os

# used for exiting the program
import sys

# import for neo4j
from neo4j import GraphDatabase
from neo4j import exceptions

def main():
    
    while True:
        main_menu()
        # enter your menu choice
        # choices are available calling the applicable functions
        choice = input("choice :")
        if choice == "1":
            view_emp_dep()

        if choice == "2":
            sal_month()

        if choice == "3":
            budg_dep()

        if choice == "4":
            add_employee()

        if choice == "5":
            show_spouse()
        
        if choice == "6":
            married()
        
        if choice == "7":
            emp_title()
        
        if choice == "X":
            exit()

# connecting to the sql database appdbproj       
conn = None

def connect():
    global conn
    conn = pymysql.connect(host="localhost", user="root",password="root",
    db="appdbproj",cursorclass=pymysql.cursors.DictCursor)
    return conn

# get employee and departments details in batches of 5 by pressing any
# key to continously get next batch of 5 records until break condition
def view_emp_dep():
    
    conn = connect()
    print("--------------")
    print("View Employees and Departments")
    print("--------------")

    # (“Read a Range of Data - LIMIT and OFFSET - SQLModel”)
    query = """
                SELECT emp.emp_no, emp.last_name, dpt.dept_no, dpt.dept_name 
                FROM employees emp
                CROSS JOIN departments dpt
                LIMIT 5 OFFSET %s;
            """
    # create a cursor object from the connection
    cursor = conn.cursor()
    # execute the query
    cursor.execute(query,(0))
    # fetch all the rows returned by the array
    rows = cursor.fetchall()
    # loop through each row 
    for x in rows:
        print (x["emp_no"], x["last_name"],x["dept_no"], x["dept_name"])
    # (“Read a Range of Data - LIMIT and OFFSET - SQLModel”)
    # setting the value that will set the print out to 5
    curr_offset = 5
    
    while True:
        # input q
        ans = input("-- Quit (q) --")
        # when q is entered and breaks
        if ans == "q":
            break
        # when not q the query is executed
        cursor.execute(query,(curr_offset))
        # fetches all related rows 
        rows = cursor.fetchall()
        # prints in the following format
        for x in rows:
            print (x["emp_no"], x["last_name"],x["dept_no"], x["dept_name"])
        # this is to set the offset to the next 5 records when any 
        # key is hit
        curr_offset = curr_offset + 5
    
# get salary month details
def sal_month():
        # starting the month value at 0 
    month_value = 0
    while True:
        input_val = input("Enter Month: ")
        # check if the value inputted is a number
        # (“Python String Isdigit() Method”)
        if input_val.isdigit():
            # setting the parameters for the input value
            if int(input_val) > 0 and int(input_val) < 13:
                month_value = input_val
                break
        # (“Python String Upper() Method”)
        # If a string month entry is chosen this function will change it
        # the entry so it is accepted by the dictionary made
        value_to_upper = input_val.upper()
        month_dict = {"JAN": 1, "FEB": 2, "MAR":3, "APR": 4, "MAY":5, "JUN" :6, "JUL":7, "AUG": 8, "SEP":9 , "OCT":10, "NOV":11, "DEC":12}
        # To retrieve the entry from the input
        month_value_from_dict = month_dict.get(value_to_upper)

        # if the month value returns this will break
        if month_value_from_dict != None:
            month_value = month_value_from_dict
            break
                  
    query = """
                SELECT FORMAT(MIN(salary),2) AS "Min", FORMAT(MAX(salary),2) AS "Max",
                FORMAT(AVG(salary),2) AS "Average Salaries"
                From salaries sal
                INNER JOIN employees emp
                on sal.emp_no = emp.emp_no
                WHERE month(emp.birth_date) = %s;
            """
    # connect to the db 

    conn = connect()

    with conn:
        cursor = conn.cursor()
        # execute the query with the month value
        cursor.execute(query,(month_value))
        # retrieves all the details
        x = cursor.fetchall()
        # Print out the answer based on month chosen
        print(x)

    
# enter a budget amount and match with the nearest department number
def budg_dep():
    
    conn = connect()
    while True:
    # enter the budget you want to check
        input_bud = input("Enter budget : ")
        if input_bud.isdigit():
            break


    # (“Sql - Find Closest Numeric Value in Database”)
    query = """
                SELECT demp.dept_no AS dept_no, COUNT(demp.emp_no) AS count
                FROM dept_emp demp 
                INNER JOIN departments dept ON demp.dept_no = dept.dept_no 
                GROUP BY demp.dept_no
                ORDER BY ABS(dept.budget - %s);
            """
    with conn:
        # create a cursor object from the connection
        cursor = conn.cursor()
        # execute the query with the variable
        cursor.execute(query,(input_bud))
        # retrieves all the records
        rows = cursor.fetchall()
        # format the values
        for x in rows:
            print(x["dept_no"], "|", x["count"])
       
    
# add a new employee to db
def add_employee():
    conn = connect()
    print("--------------")
    print("Add New Employee")
    print("--------------")
    # insert all values with the %s argument to allow strings
    query = "INSERT INTO employees() VALUES (%s,%s,%s,%s,%s,%s)"

    with conn:
        while True:
            try:
                # enter all the required inputs to add new employee
                emp_no = input("Emp No: ")
                first_name = input("First Name: ")
                last_name = input("Last Name: ")
                gender = input("Gender: ")
                birth_date = input("Birth date (YYYY-MM-DD): ")
                hire_date = input("Hire date (YYYY-MM-DD): ")
                cursor = conn.cursor()

                # convert birth_date and hire_date to correct format
                birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
                hire_date = datetime.strptime(hire_date, '%Y-%m-%d')

                cursor.execute(query, (emp_no,birth_date,first_name,last_name,gender,hire_date))
                # to add a new employee to the database
                conn.commit()
                print()
                # once completed it breaks and returns to the menu
                break
                menu()
            # this will prompt the user to enter correct date
            # if there is an error along with excpetion (e)
            # (“8. Errors and Exceptions — Python 3.8.1 Documentation”)
            except ValueError as e:
                print("Error:", e)
                print("Please enter a date in the format YYYY-MM-DD")
            # handles an internal error in the mypysql library
            except pymysql.err.InternalError as e:
                print("Internal Error:", e)
            # exeption if the entry already exist
            except pymysql.err.IntegrityError:
                print("*** ERROR ***", e, "already exists")
            # handles any other exception not caught
            except Exception as e:
                print("Error:", e)

# get the employee number and title for an employee,
# publish to file
def emp_title():

    conn = connect()

    # define the file path    
    employee_titles = "employee_titles.txt"  
    
    query = """
                SELECT emp.emp_no AS Employee_Number, tt.title AS Title
                FROM employees emp
                inner join titles tt
                on emp.emp_no = tt.emp_no
                ORDER BY Employee_Number, Title;
                
            """
    # (“OS Module in Python with Examples”)
    # if the path does not exist create employee_titles
    if not os.path.exists(employee_titles):
        # writes the contents
        with open(employee_titles, "w") as f:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            # this is format of the file
            for x in rows:
                f.write(str(x["Employee_Number"]) + "|" + str(x["Title"]) + "\n")
        print("File created: ", employee_titles)
    # when the files exists
    else:
        print("File already exists")
        # reads the file
        with open(employee_titles, "r") as f:
            for line in f:
                # strip method removes any whitespace characters
                # (“How Does Raw_input().Strip().Split() in Python Work in This Code?”)
                employee_number, title = line.strip().split("|")
                print(employee_number, title)


# connecting to neo4j database
driver = None

def connect_neo():
    global driver
    uri = "neo4j://localhost:7687"
    driver = GraphDatabase.driver(uri,auth= ("neo4j", "neo4jneo4j"), max_connection_lifetime=1000)
    return driver 

# Matches the user inputted to get their spouse details.
def show_spouse():
    if not driver:
        connect_neo()
    # user prompted to enter emp number
    emp_number = input("Enter Employee Number: ")
    # check who the employee is married too
    query = """
                MATCH (e:Employee{emp_no:$emp_no})-[:MARRIED_TO]->(spouse)
                RETURN spouse.emp_no AS spouse
            """
    # (“API Documentation — Neo4j Python Driver 5.7”)
    with driver.session() as session:
        # run the query
        result = session.run(query, emp_no=int(emp_number))
        # this pulls the record
        if result.peek():
            # reference of the record
            spouse_emp_no = result.single()[0]
            print("Spouse of: " + str(spouse_emp_no))
            spouse_details(spouse_emp_no= spouse_emp_no)

# When the spouse is returned,  this function pulls out the details.    
def spouse_details(spouse_emp_no):
    conn = connect()
    # get the spouse details
    sqlquery = "SELECT emp.emp_no, emp.first_name, emp.last_name FROM employees emp WHERE emp_no=%s;"
   
    cursor = conn.cursor()

    # Execute the SQL query with the input parameter
    cursor.execute(sqlquery, int(spouse_emp_no))

    # Fetch the results
    results = cursor.fetchall()
    # print out in the format
    for row in results:
        print(row["emp_no"],"|", row["first_name"], "|", row["last_name"]) 
    
# this creates the relationship of married for employees
def married():
    if not driver:
        connect_neo()
    
    while True:
        # prompt the user to enter the numbers to be queried
        emp1 = input("Enter 1st Employee Number: ")
        emp2 = input("Enter 2nd Employee Number: ")

        def just_married_tx(tx):
            # Query to create the relationship, married to
            # (“API Documentation — Neo4j Python Driver 5.8”)
            query = "MATCH (e1:Employee {emp_no: $emp1}), (e2:Employee {emp_no: $emp2}) CREATE (e1)-[:MARRIED_TO]->(e2)"
            
            result = tx.run(query, emp1=int(emp1), emp2=int(emp2))
        

        # check if both users exist in the database
        with driver.session() as session:
            # this takes the emp number entered and matches it. the match clause is returned with the boolean value.
            result1 = session.run("MATCH (e:Employee {emp_no: $emp1}) RETURN COUNT(e) > 0 AS emp_exists", emp1 = int(emp1)).single()
            result2 = session.run("MATCH (e:Employee {emp_no: $emp2}) RETURN COUNT(e) > 0 AS emp_exists", emp2 = int(emp2)).single()
            # if either doests the error message returns that they don't exist
            if not result1['emp_exists'] or not result2['emp_exists']:
                print(f"Error: Employee {emp1} or {emp2} not found in database.")
                continue
            # checks if the employees are married
            result = session.run("MATCH (:Employee {emp_no: $emp1})-[:MARRIED_TO]->(:Employee {emp_no: $emp2}) RETURN COUNT(*) as count", emp1 = int(emp1), emp2 = int(emp2))
            # using the python integer values to check if true or false
            # so if 0 is the answer it will return the emp is already married
            if result.single()["count"] > 0:
                print(f"{emp1} and {emp2} are already married.")
            else:
                # when the employees exist, the query runs to create the relationship
                session.execute_write(just_married_tx)
                print(f"{emp1} is now married to {emp2}")
            break


def exit():
    # exit the application
    sys.exit()    

# the menu the user will see when accessing the program
def main_menu():
    print("MENU\n===")
    print("1 - View Employees & Departments")
    print("2 - View Salary Details")
    print("3 - View Departments by Budget")
    print("4 - Add New Employee")
    print("5 - Find an Employee's Spouse")
    print("6 - Add Marriage Details")
    print("7 - View Employee Titles")
    print("x - Exit application")

if __name__ == "__main__":
	main()


