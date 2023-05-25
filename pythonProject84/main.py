import psycopg2


class Table:
    def __init__(self):
        with psycopg2.connect(dbname="homework", user="postgres", password="lenochka77", host='localhost', port='5432') as conn:
            self.cursor = conn.cursor()

    def drop_tables(self, name_of_table):
        self.cursor.execute("""
            DROP TABLE name_of_table=%s;
            """, name_of_table)
        conn.commit()

    def create_table(self, conn, name_of_table: str, column1, column2, column3=None, column4=None):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS name_of_table=%s(
            column1=%s SERIAL PRIMARY KEY,
            column2=%s VARCHAR(40),
            column3=%s VARCHAR(40) UNIQUE,
            column4=%s INTEGER
            );
            """, (name_of_table, column1, column2, column3, column4))
        return self.cursor.fetchall()


    def add_client(self, conn, first_name, surname, email, phones_number=None):
        self.cursor.execute("""
            INSERT INTO clients(first_name, surname, email)
            VALUES (%s, %s, %s)
            RETURNING id, first_name, surname, email;     
            """, (first_name, surname, email))
        return self.cursor.fetchone()


    def add_phone(self, conn, client_id, phone_id, phone_number):
        self.cursor.execute("""
            UPDATE phone_numbers SET phone_number=%s WHERE client_id=%s AND phone_id=%s;
            """, (client_id, phone_id, phone_number))
        return self.cursor.fetchone()


    def change_client(self, conn, client_id, first_name=None, surname=None, email=None, phone_number=None):
        self.cursor.execute("""
            UPDATE clients SET first_name = %s, surname = %s, 
            email = %s, phone_number = %s WHERE client_id=%s;
            """, (client_id, first_name, surname, email, phone_number))
        return self.cursor.fetchone()


    def delete_phone(self, conn, client_id, phone_number):
        self.cursor.execute("""
                DELETE FROM phone_numbers WHERE client_id=%s AND phone_number=%s;
                """, (client_id, phone_number))
        return self.cursor.fetchone()


    def delete_client(self, conn, client_id):
        self.cursor.execute("""
                DELETE FROM phone_numbers WHERE client_id=%s;
                DELETE FROM clients WHERE client_id=%s;
                """, (client_id,))
        conn.commit()

    def find_client(self, cursor, conn, first_name=None, surname=None, email=None, phone_number=None):
        self.cursor.execute("""
                SELECT DISTINCT first_name, surname FROM clients
                WHERE first_name=%s OR surname=%s OR email=%s OR phone_number=%s
                """, (first_name, surname, email, phone_number))
        return self.cursor.fetchone()


with psycopg2.connect(dbname="homework", user="postgres", password="lenochka77") as conn:
    data = Table()
    data.find_client(conn, 'Lavreneva')


conn.close()
