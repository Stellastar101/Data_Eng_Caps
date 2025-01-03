import mysql.connector 
from mysql.connector import pooling
dbconfig = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "my_password",
    "database": "little_lemon_db"
}
pool = pooling.MySQLConnectionPool(
    pool_name= "my_pool",
    pool_size=2,
    **dbconfig  
)

connection = pool.get_connection()
cursor = connection.cursor()

#Create and call a stored procedure named PeakHours that identifies the peak, or busiest hour, for the restaurant based on the number of bookings.
cursor.execute("USE little_lemon_db")
create_procedure_PeakHours =  """
    DELIMITER //
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
    END //
    DELIMITER ;
    """
cursor.execute("DROP PROCEDURE IF EXISTS PeakHours")
cursor.execute(create_procedure_PeakHours)
cursor.callproc('PeakHours')
for result in cursor.stored_results():
    results = result.fetchall()
    column_names = result.column_names
print("Column Names:", results)


#Create and call a stored procedure named GuestStatus that outputs status of each guest’s order based on which employee is assigned to the order.
'''
cursor.execute("SELECT * FROM employees")
employees = cursor.fetchall() 
for employee in employees:
    print(employee)
'''