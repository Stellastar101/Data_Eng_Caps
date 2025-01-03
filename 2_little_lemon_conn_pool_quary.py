#TASK 1

import mysql.connector
from mysql.connector import pooling, Error


tasks = ["Task 1","Task 2","Task 3","Task 4","Task 5"]
task1 = "\033[4m" + tasks[0] + "\033[0m"
task2 = "\033[4m" + tasks[1] + "\033[0m"
task3 = "\033[4m" + tasks[2] + "\033[0m"
task4 = "\033[4m" + tasks[3] + "\033[0m"
task5 = "\033[4m" + tasks[4] + "\033[0m"
print(task1)


# Step 1: Define your database configurations in a dictionary
dbconfig = {
    "host": "localhost",
    "user": "root",
    "password": "my_password",
    "database": "little_lemon_db"
}

# Step 2: Create a connection pool
try:
    pool_b = pooling.MySQLConnectionPool(
        pool_name="pool_b",
        pool_size=2,
        **dbconfig
    )
    print(f'Connection pool created successfully: Pool name: {pool_b.pool_name}')
    print(f'Pool size, {pool_b.pool_size}')
except Error as err:
    print(f"Error: {err}")
    print(f'Type the correct syntax')

def connection_reserve():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="my_password",
            database="little_lemon_db"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error creating direct connection: {err}")
        return None
#Task 2
##############################################################################################
print(task2)
def insert_booking(connection, table_number, first_name, last_name, booking_time, employee_id):
    cursor = connection.cursor()
    query = """
    INSERT INTO Bookings (TableNo, GuestFirstName, GuestLastName, BookingSlot, EmployeeID)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (table_number, first_name, last_name, booking_time, employee_id))
    connection.commit()
    cursor.close()

'''
try:
    connection_1 = pool_b.get_connection()
    connection_2 = pool_b.get_connection()
    
    insert_booking(connection_1, 8, "Anees", "Java", "18:00", 6)
    insert_booking(connection_2, 5, "Bald", "Vin", "19:00", 6)
    connection_3 = connection_reserve()
    if connection_3:
        insert_booking(connection_3, 12, "Jay", "Kon", "19:30", 6)
except mysql.connector.pooling.PoolError as pool_err:
    print(f"Pool Error: {pool_err}")
finally:
    if 'connection_1' in locals():
        connection_1.close()
    if 'connection_2' in locals():
        connection_2.close()
    if 'connection_3' in locals() and connection_3:
        connection_3.close()
'''
#Task 3

##########################################################################################
print(task3)
def generate_report(connection):
    cursor = connection.cursor(dictionary=True)
    
    # Query to get the manager's name and EmployeeID
    cursor.execute("SELECT Name, EmployeeID FROM Employees WHERE Role = 'Manager' LIMIT 1")
    manager = cursor.fetchone()
    
    # Query to get the employee with the highest salary
    cursor.execute("""
    SELECT Name, Role, Annual_Salary 
    FROM Employees 
    INNER JOIN (SELECT MAX(Annual_Salary) AS Max_Salary FROM Employees) AS MaxSalary 
    ON Employees.Annual_Salary = MaxSalary.Max_Salary;
      """)
    highest_salary_employee = cursor.fetchone()
    
    # Query to count the number of bookings between 18:00 and 20:00
    cursor.execute("""SELECT COUNT(*) AS Number_Of_Guests FROM Bookings WHERE BookingSlot BETWEEN '18:00:00' AND '20:00:00'""")
    guest_count = cursor.fetchone()['Number_Of_Guests']
    
    # Query to get guests waiting to be seated (assuming status is 'Waiting')


    #########
    stored_procedure_query="""
        DELIMITER //

    CREATE PROCEDURE GuestStatus()
    BEGIN
        SELECT 
        Bookings.BookingID AS BookingID,  
        CONCAT(GuestFirstName, ' ', GuestLastName) AS GuestName, 
        Role AS Employee, 
        CASE 
            WHEN Role IN ('Manager','Assistant Manager') THEN "Ready to Pay"
            WHEN Role = 'Head Chef' THEN "Ready to serve"
            WHEN Role = 'Assistant Chef' THEN "Preparing order"
            WHEN Role = 'Head Waiter' THEN "Order served"
            WHEN Role = 'receptionist' THEN "waiting"
            ELSE "Pending"
        END AS Status
        FROM Bookings 
        LEFT JOIN 
        Employees 
        ON Employees.EmployeeID = Bookings.EmployeeID;
    END //

    DELIMITER ;
    """
    cursor.callproc('GuestStatus')
    results = next(cursor.stored_results())
    Guests_status = results.fetchall()
    #data = [order for order in Guests_status if order['Status'] == 'waiting']
  
    cursor.close()
    
    # Print the report
    print(f"Manager: {manager['Name']} (EmployeeID: {manager['EmployeeID']})")
    print(f"Highest Salary Employee: {highest_salary_employee['Name']} - {highest_salary_employee['Role']} - Salary: {highest_salary_employee['Annual_Salary']}")
    print(f"Number of guests booked between 18:00 and 20:00: {guest_count}")
    print(f'Guests waiting to be seated:')
    for guests in Guests_status:
        if guests['Status'] == 'waiting':
            print(f"{guests['GuestName']}|BookingID: {guests['BookingID']} | Status: {guests['Status']}")
    print("++++++++++++++++++++++++++")

# Get a connection from the pool and generate the report
connection = pool_b.get_connection()
generate_report(connection)
connection.close()


# Task 4

#############################################################
##  NOT FINISHED TASK 4 ###
print(task4)
basic_report_procedure = '''
                DROP PROCEDURE IF EXISTS BasicSalesReport
                DELIMITER //

                CREATE PROCEDURE  BasicSalesReport()
                BEGIN
                    SELECT 
                    SUM(BillAmount) AS Total_Sales,
                    ROUND(AVG(BillAmount)) AS Average_Sale, 
                    MAX(BillAmount) AS Max_Sale,
                    MIN(BillAmount) AS Min_Sale
                FROM Orders;
                END //

                DELIMITER ; '''

connection_1 = pool_b.get_connection()
cursor = connection_1.cursor()
try:
    cursor.callproc('BasicSalesReport')
    report = next(cursor.stored_results())
    column_names = [desc[0] for desc in report.description]
    print(" | ".join(column_names))  # Print columns from report
    for row in report.fetchall():
        print(" | ".join(map(str, row)))

finally:
    cursor.close()
    connection_1.close()

# 
# TASK 5
###########################################################################################
print(task5)
def display_upcoming_bookings(connection):
    cursor = connection.cursor(dictionary=True)
    
    # Query to get the next 3 upcoming bookings
    cursor.execute("""
    SELECT b.BookingID, b.GuestFirstName, b.GuestLastName, b.BookingSlot, e.Name AS EmployeeName
    FROM Bookings b
    JOIN Employees e ON b.EmployeeID = e.EmployeeID
    ORDER BY b.BookingSlot ASC
    LIMIT 3
    """)
    
    bookings = cursor.fetchall()
    for booking in bookings:
        print(f"BookingID: {booking['BookingID']}, Name: {booking['GuestFirstName']} {booking['GuestLastName']}, BookingSlot: {booking['BookingSlot']}, Assigned to: {booking['EmployeeName']}")
    
    cursor.close()

# Get a connection from the pool and display the upcoming bookings
connection = pool_b.get_connection()
display_upcoming_bookings(connection)
connection.close()

