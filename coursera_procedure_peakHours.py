import mysql.connector

# Database connection
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'my_password',
    'database': 'little_lemon_db'
}


# Step 1: Establish connection
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()
# Step 2: Switch to the database
cursor.execute("USE little_lemon_db")
# Step 3: Create the stored procedure
create_procedure_PeakHours = """
CREATE PROCEDURE PeakHours()
BEGIN
    SELECT 
        HOUR(BookingSlot) AS BookingHour,
        COUNT(*) AS NumberOfBookings
    FROM 
        Bookings
    GROUP BY 
        BookingHour
    ORDER BY 
        NumberOfBookings DESC;
END
    """
cursor.execute("DROP PROCEDURE IF EXISTS PeakHours")
cursor.execute(create_procedure_PeakHours)
# Step 4: Call the stored procedure
cursor.callproc('PeakHours')
# Step 5: Fetch results
for result in cursor.stored_results():
    results = result.fetchall()
    column_names = result.column_names
# Step 6: Print column names
print("Column Names:", column_names)
# Step 7: Print sorted data
print("Peak Hours Data:")
for row in results:
    print(row)
cursor.close()

