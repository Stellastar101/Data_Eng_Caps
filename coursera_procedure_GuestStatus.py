import mysql.connector

# Database connection
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'my_password',
    'database': 'little_lemon_db'
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

cursor.execute("USE little_lemon_db")

create_procedure_GuestStatus = """
CREATE PROCEDURE GuestStatus()
BEGIN
    SELECT 
        SELECT CONCAT(GuestFirstName, GuestLastName) AS FullName FROM Bookings
END
    """
cursor.execute("DROP PROCEDURE IF EXISTS GuestStatus")
cursor.execute(create_procedure_GuestStatus)

cursor.callproc('GuestStatus')

for result in cursor.stored_results():
    results = result.fetchall()
    column_names = result.column_names

print("Column Names:", column_names)

print("GuestStatus:")
for row in results:
    print(row)
cursor.close()

