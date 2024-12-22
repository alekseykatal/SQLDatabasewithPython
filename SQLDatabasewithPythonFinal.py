import sqlite3


# creates the Employee table if it doesnt exist
def createEmployeeTable(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Employee (
        EmployeeID INTEGER PRIMARY KEY,
        Name TEXT
    )
    ''')
    # print("Employee table created.")


# creates the Pay table if it doesnt exist
def createPayTable(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Pay (
        EmployeeID INTEGER,
        Year INTEGER,
        Earnings REAL,
        FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
    )
    ''')
    # print("Pay table created.")


# creates the SocialSecurityMin table if it doesnt exist
def createSocialSecurityMinTable(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS SocialSecurityMin (
        Year INTEGER PRIMARY KEY,
        Minimum REAL
    )
    ''')
    # print("SocialSecurityMin table created.")


# adds employee data from a file to the Employee table
def addEmployeeData(filename, cursor):
    with open(filename, 'r') as file:
        next(file)  # skips the first line
        for line in file:
            employee_id, name = line.strip().split(',')
            cursor.execute('INSERT INTO Employee (EmployeeID, Name) VALUES (?, ?)', (employee_id, name))
    # print("Employee data inserted.")


# adds pay data from a file into the Pay table
def addPay(filename, cursor):
    with open(filename, 'r') as file:
        next(file)  # skips the first line
        for line in file:
            employee_id, year, earnings = line.strip().split(',')
            cursor.execute('INSERT INTO Pay (EmployeeID, Year, Earnings) VALUES (?, ?, ?)', (employee_id, year, earnings))
    # print("Pay data inserted.")


# adds social security minimum data from a file to the SocialSecurityMin table
def addSocialSecurityMin(filename, cursor):
    with open(filename, 'r') as file:
        next(file)  # skips the first line
        for line in file:
            year, minimum = line.strip().split(',')
            cursor.execute('INSERT INTO SocialSecurityMin (Year, Minimum) VALUES (?, ?)', (year, minimum))
    # print("Social Security Minimum data inserted.")


# joins the Employee, Pay, and SocialSecurityMin tables
def joinTables(cursor):
    cursor.execute('''
    SELECT 
        E.EmployeeID, 
        E.Name, 
        P.Year, 
        P.Earnings, 
        S.Minimum
    FROM 
        Employee E
    INNER JOIN 
        Pay P ON E.EmployeeID = P.EmployeeID
    INNER JOIN 
        SocialSecurityMin S ON P.Year = S.Year;
    ''')


# displays the final results
def displayResults(cursor):
    rows = cursor.fetchall()

    # reverses the output
    revered_rows = reversed(rows)

    # prints out the header for the Output
    print(f"{'Employee Name':<25}{'Year':<10}{'Earnings':<20}{'Minimum':<20}{'Include'}")
    print(f"<", "-" * 80, ">")

    # loops through the rows and formats the data for display
    for row in revered_rows:
        employee_id, name, year, earnings, minimum = row
        earnings_formatted = f"{earnings:,.2f}"
        minimum_formatted = f"{minimum:,.2f}"
        include = "Yes" if earnings >= minimum else "No"

        # prints each row of data
        print(f"{name:<25}{year:<10}{earnings_formatted:<20}{minimum_formatted:<20}{include}")


# main function that calls the other functions
def main():

    # connects to the SQLite database
    dbConnection = sqlite3.connect("database.db")

    # creates a cursor object to execute the SQL commands
    cursor = dbConnection.cursor()

    # drops the tables each time to start fresh
    # cursor.execute('DROP TABLE IF EXISTS Employee')
    # cursor.execute('DROP TABLE IF EXISTS Pay')
    # cursor.execute('DROP TABLE IF EXISTS SocialSecurityMin')

    # creates the tables
    createEmployeeTable(cursor)
    createPayTable(cursor)
    createSocialSecurityMinTable(cursor)

    # adds the correct data from the files into the tables
    addEmployeeData('Employee.txt', cursor)
    addPay('Pay.txt', cursor)
    addSocialSecurityMin('SocialSecurityMinimum.txt', cursor)

    # commits the changes to the database
    dbConnection.commit()

    # joins the tables
    joinTables(cursor)

    # displays the results
    displayResults(cursor)

    # closes the database connection
    dbConnection.close()


# calls the main function
main()
