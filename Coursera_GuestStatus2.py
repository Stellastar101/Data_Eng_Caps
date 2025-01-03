import mysql.connector

# Database connection
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'my_password',
    'database': 'little_lemon_db'
}

try:
    # Step 1: Establish connection
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Step 2: Create stored procedure
    create_procedure_GuestStatus = """
    CREATE PROCEDURE GuestStatus()
    BEGIN
        SELECT 
            CONCAT(Guests.FirstName, ' ', Guests.LastName) AS GuestName,
            CASE 
                WHEN Employees.Role IN ('Manager', 'Assistant Manager') THEN 'Ready to pay'
                WHEN Employees.Role = 'Head Chef' THEN 'Ready to serve'
                WHEN Employees.Role = 'Assistant Chef' THEN 'Preparing Order'
                WHEN Employees.Role = 'Head Waiter' THEN 'Order served'
                ELSE 'Unknown'
            END AS OrderStatus
        FROM 
            Bookings
        LEFT JOIN Employees ON Bookings.EmployeeID = Employees.EmployeeID
        LEFT JOIN Guests ON Bookings.GuestID = Guests.GuestID;
    END;
    """
    cursor.execute("DROP PROCEDURE IF EXISTS GuestStatus")
    cursor.execute(create_procedure_GuestStatus)

    # Step 3: Call the stored procedure
    cursor.callproc('GuestStatus')

    # Step 4: Fetch results
    for result in cursor.stored_results():
        dataset = result.fetchall()
        column_names = result.column_names

    # Step 5: Print column names
    print("Column Names:", column_names)

    # Step 6: Print sorted data
    print("Guest Status Data:")
    for row in dataset:
        print(row)

except mysql.connector.Error as e:
    print(f"Error: {e}")

finally:
    # Step 7: Close the connection
    if cursor:
        cursor.close()
    if conn:
        conn.close()