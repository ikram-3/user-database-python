import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='user',
                user='root',
                password=''
            )
            if self.connection.is_connected():
                db_info = self.connection.get_server_info()
                print("Connected to MySQL Server version", db_info)
                cursor = self.connection.cursor()
                cursor.execute("SELECT DATABASE();")
                record = cursor.fetchone()
                print("You're connected to database:", record)
        except Error as e:
            print("Error while connecting to MySQL:", e)
            self.connection = None

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")
        else:
            print("MySQL connection is already closed or not established")

    def create_user(self):
        name = input("Enter your name: ")
        age = input("Enter your age: ")
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user (
                    name VARCHAR(255),
                    age INT,
                    email VARCHAR(255),
                    password VARCHAR(255)
                )
            """)
            cursor.execute("INSERT INTO user (name, age, email, password) VALUES (%s, %s, %s, %s)", (name, age, email, password))
            self.connection.commit()
            print("User created successfully")
        except Error as e:
            print("Error while creating table or inserting data:", e)

    def read_users(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM user")
            records = cursor.fetchall()
            print("Total number of users:", cursor.rowcount)
            for row in records:
                print(f"Name: {row[0]}, Age: {row[1]}, Email: {row[2]}, Password: {row[3]}")
        except Error as e:
            print("Error while reading table:", e)

    def update_user(self):
        name = input("Enter your name: ")
        age = input("Enter your age: ")
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        try:
            cursor = self.connection.cursor()
            cursor.execute("UPDATE user SET age = %s, email = %s, password = %s WHERE name = %s", (age, email, password, name))
            self.connection.commit()
            print("User updated successfully")
        except Error as e:
            print("Error while updating user:", e)

    def delete_user(self):
        name = input("Enter your name to delete: ")
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM user WHERE name = %s", (name,))
            self.connection.commit()
            print("User deleted successfully")
        except Error as e:
            print("Error while deleting user:", e)
