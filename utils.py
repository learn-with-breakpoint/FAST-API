import psycopg2
import psycopg2.extras


class BookDatabaseConnection:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = self.get_connection()

    def get_connection(self):
        try:
            connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return connection
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None

    def execute_query(self, query, params=None,
                      fetchall=True, commit=False):
        cursor = None
        if not self.connection:
            self.connection = self.get_connection()
        try:
            cursor = self.connection.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute(query, params)
            if commit:
                self.connection.commit()
            if fetchall:
                rows = cursor.fetchall()
            else:
                rows = cursor.fetchone()
            return rows
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None
        finally:
            if cursor:
                cursor.close()

    def close_connection(self):
        if self.connection:
            try:
                self.connection.close()
                print("Connection closed")
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)


# Example usage:
if __name__ == "__main__":
    host = "localhost"
    database = "bookstore"
    user = "admin"
    password = "LocalPasswordOnly"

    book_db = BookDatabaseConnection(host, database, user, password)

    query = "SELECT * FROM books"
    params = None
    rows = book_db.execute_query(query, params)

    if rows:
        for row in rows:
            print(row)
    else:
        print("Query execution failed")
    book_db.close_connection()


def dict_to_query(in_dict: dict) -> list:
    query = []
    values = []
    for k, v in in_dict.items():
        if v is not None:
            query.append(k)
            values.append(v)
    query.extend(values)
    return query
