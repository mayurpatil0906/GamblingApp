from db.queries import ALL_TABLES

def create_all_tables(connection):
    cursor = connection.cursor()

    try:
        for query in ALL_TABLES:
            cursor.execute(query)
        connection.commit()
        print("All tables created successfully.")
    except Exception as e:
        print(e)
    finally:
        cursor.close()