from mysql.connector import connect


def create_connection():
    try:
        cnx = connect(
            host='localhost',
            database='sanjana',
            user='root',
            password='kjs2022'
        )
        return cnx
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
