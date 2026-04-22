import mysql.connector
from mysql.connector import Error
from db.db_config import DB_CONFIG


def create_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
            port=DB_CONFIG["port"]
        )
        if connection.is_connected():
            print("Connected to MySQL successfully.")
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None