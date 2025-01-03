# Import MySQL Connector/Python
import mysql.connector as connector

# Establish connection to MySQL
connection = connector.connect(user="your_username", password="your_password")
cursor = connection.cursor()

# Create the database
cursor.execute("CREATE DATABASE IF NOT EXISTS little_lemon_db")
cursor.execute("USE little_lemon_db")

# MenuItems table
create_menuitem_table = """CREATE TABLE MenuItems (
    ItemID INT AUTO_INCREMENT,
    Name VARCHAR(200),
    Type VARCHAR(100),
    Price INT,
    PRIMARY KEY (ItemID)
);"""

# Menus table
create_menu_table = """CREATE TABLE Menus (
    MenuID INT,
    ItemID INT,
    Cuisine VARCHAR(100),
    PRIMARY KEY (MenuID, ItemID),
    FOREIGN KEY (ItemID) REFERENCES MenuItems(ItemID)
);"""

# Orders table
create_orders_table = """CREATE TABLE Orders (
    OrderID INT,
    TableNo INT,
    MenuID INT,
    BookingID INT,
    Quantity INT,
    BillAmount INT,
    PRIMARY KEY (OrderID, TableNo),
    FOREIGN KEY (MenuID) REFERENCES Menus(MenuID)
);"""

# Employees table
create_employees_table = """CREATE TABLE Employees (
    EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255),
    Role VARCHAR(100),
    Address VARCHAR(255),
    Contact_Number INT,
    Email VARCHAR(255),
    Annual_Salary VARCHAR(100)
);"""

# Create tables
tables = [create_menuitem_table, create_menu_table, create_orders_table, create_employees_table]
for table in tables:
    cursor.execute(table)
    print(f'Table created: {table.split()[2]}')

# Insert data into MenuItems
insert_menuitems = """
INSERT INTO MenuItems (Name, Type, Price)
VALUES
('Olives','Starters',5),
('Flatbread','Starters', 5),
('Minestrone', 'Starters', 8),
('Tomato bread','Starters', 8),
('Falafel', 'Starters', 7),
('Hummus', 'Starters', 5),
('Greek salad', 'Main Courses', 15),
('Bean soup', 'Main Courses', 12),
('Pizza', 'Main Courses', 15),
('Greek yoghurt','Desserts', 7),
('Ice cream', 'Desserts', 6),
('Cheesecake', 'Desserts', 4),
('Athens White wine', 'Drinks', 25),
('Corfu Red Wine', 'Drinks', 30),
('Turkish Coffee', 'Drinks', 10),
('Turkish Coffee', 'Drinks', 10),
('Kabasa', 'Main Courses', 17);
"""
cursor.execute(insert_menuitems)
print("MenuItems table populated")
connection.commit()

# Insert data into Menus
insert_menu = """
INSERT INTO Menus (MenuID, ItemID, Cuisine)
VALUES
(1, 1, 'Greek'),
(1, 7, 'Greek'),
(1, 10, 'Greek'),
(1, 13, 'Greek'),
(2, 3, 'Italian'),
(2, 9, 'Italian'),
(2, 12, 'Italian'),
(2, 15, 'Italian'),
(3, 5, 'Turkish'),
(3, 17, 'Turkish'),
(3, 11, 'Turkish'),
(3, 16, 'Turkish');
"""
cursor.execute(insert_menu)
print("Menus table populated")
connection.commit()

# Insert data into Orders
insert_orders = """
INSERT INTO Orders (OrderID, TableNo, MenuID, BookingID, Quantity, BillAmount)
VALUES
(1, 12, 1, 1, 2, 86),
(2, 19, 2, 2, 1, 37),
(3, 15, 2, 3, 1, 37),
(4, 5, 3, 4, 1, 40),
(5, 8, 1, 5, 1, 43);
"""
cursor.execute(insert_orders)
print("Orders table populated")
connection.commit()

# Insert data into Employees
insert_employees = """
INSERT INTO Employees (Name, Role, Address, Contact_Number, Email, Annual_Salary)
VALUES
('Mario Gollini','Manager','724, Parsley Lane, Old Town, Chicago, IL',351258074,'Mario.g@littlelemon.com','$70,000'),
('Adrian Gollini','Assistant Manager','334, Dill Square, Lincoln Park, Chicago, IL',351474048,'Adrian.g@littlelemon.com','$65,000'),
('Giorgos Dioudis','Head Chef','879 Sage Street, West Loop, Chicago, IL',351970582,'Giorgos.d@littlelemon.com','$50,000'),
('Fatma Kaya','Assistant Chef','132 Bay Lane, Chicago, IL',351963569,'Fatma.k@littlelemon.com','$45,000'),
('Elena Salvai','Head Waiter','989 Thyme Square, EdgeWater, Chicago, IL',351074198,'Elena.s@littlelemon.com','$40,000'),
('John Millar','Receptionist','245 Dill Square, Lincoln Park, Chicago, IL',351584508,'John.m@littlelemon.com','$35,000');
"""
cursor.execute(insert_employees)
print("Employees table populated")
connection.commit()
