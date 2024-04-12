import psycopg2

from config import host, user, password, dbname


def my_decorator(func):
    def wrapper(*args, **kwargs):
        global connection
        try:
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=dbname,
            )
            connection.autocommit = True
            func(*args, **kwargs)
        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")

    return wrapper


@my_decorator
def create_table():
    with connection.cursor() as cursor:
        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                            id serial PRIMARY KEY,
                            first_name VARCHAR(50) NOT NULL,
                            nick_name VARCHAR(50) NOT NULL);""")

        print(f"Table create successfully")


@my_decorator
def insert_data(first_name, nick_name):
    with connection.cursor() as cursor:
        cursor.execute("""INSERT INTO users (first_name, nick_name) VALUES (%s, %s);""", (first_name, nick_name))

        print(f"Data was successfully inserted")


@my_decorator
def get_data(first_name):
    with connection.cursor() as cursor:
        cursor.execute("""SELECT nick_name FROM users WHERE first_name = %s;""", (first_name,))
        result = cursor.fetchone()
        if result:
            print(result[0])
        else:
            print("No data found for the specified first name.")


@my_decorator
def drop_table():
    with connection.cursor() as cursor:
        cursor.execute("""DROP TABLE users;""")

        print("[INFO] Table was deleted")


if __name__ == '__main__':
    create_table()
    insert_data("First Name", "Nickname")
    get_data("First Name")
    # drop_table()


