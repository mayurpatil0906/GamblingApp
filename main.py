from db.db_connection import create_connection
from db.create_tables import create_all_tables


def main():
    connection = create_connection()

    if connection is not None:
        create_all_tables(connection)
        connection.close()
        print("Database connection closed.")
    else:
        print("Could not connect to database.")


if __name__ == "__main__":
    main()