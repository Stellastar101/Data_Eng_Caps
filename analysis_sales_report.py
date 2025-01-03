import mysql.connector 
from mysql.connector import pooling
dbconfig = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "my_password",
    "database": "little_lemon_db"
}
pool_b = pooling.MySQLConnectionPool(
    pool_name= "pool_b",
    pool_size=2,
    **dbconfig  
)

try:
    pool_b = pooling.MySQLConnectionPool(
        pool_name="pool_b",
        pool_size=2,
        **dbconfig
    )
    print("Connection pool created successfully.")
except Error as err:
    print(f"Error: {err}")

'''
Table Number: 8

First Name: Anees

Last Name: Java

Booking Time: 18:00

EmployeeID: 6
'''

# TASK 2 
#Three guests are trying to book dinner slots simultaneously. Get the connections from pool_b and insert the following data in the Bookings table:
def insert_booking(connection, table_number, first_name, last_name, booking_time, EmployeeID):
    cursor.connection.cursor()
    insert_bookings_query = """INSERT INTO Bookings (BookingID, TableNo, GuestFirstName, GuestLastName, BookingSlot, EmployeeID) VALUES(%s, %s, %s, %s, %s, %s) """
    cursor.execute(insert_booking,(table_number, first_name, last_name, booking_time, EmployeeID))
    connection.commit()
    cursor.close()

try:
    conne_1 = pool_b.get_connection()
    conn_2 = pool_b.get_connection()

    insert_booking(conn_1, 8, "Anees", "Java", "18:00", 6)
    insert_booking(conn_2, 5, "Bald", "Vin", "19:00", 6)

    con

    