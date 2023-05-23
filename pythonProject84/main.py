import psycopg2

class Table():
    def drop_tables(self, name_of_table):
        with conn.cursor() as self.cur:
            self.cur.execute("""
                    DROP TABLE name_of_table=%s;
                    """, name_of_table)

    def create_table(self, conn, name_of_table: str, column1, column2, column3=None, column4=None):
        with conn.cursor() as self.cur:
            self.cur.execute("""
                   CREATE TABLE IF NOT EXISTS name_of_table=%s(
                   column1=%s SERIAL PRIMARY KEY,
                   column2=%s VARCHAR(40),
                   column3=%s VARCHAR(40) UNIQUE,
                   column4=%s INTEGER
                   );
                   """, (name_of_table, column1, column2, column3, column4))
            return self.cur.fetchall()

    def add_client(self, conn, name, lastname, email, phones_number=None):
        with conn.cursor() as self.cur:
            self.cur.execute("""
                INSERT INTO clients(name, lastname, email)
                VALUES (%s, %s, %s)
                RETURNING id, name, lastname, email;     
                """, (name, lastname, email))
        return self.cur.fetchone()

    def add_phone(self, conn, client_id, phone_id, phone_number):
        with conn.cursor() as self.cur:
            self.cur.execute("""
                    UPDATE phone_numbers SET phone_number=%s WHERE client_id=%s AND phone_id=%s;
                    """, (client_id, phone_id, phone_number))
        return self.cur.fetchone()

    def change_client(self, conn, client_id, first_name=None, surname=None, email=None, phone_number=None):
        with conn.cursor() as self.cur:
            self.cur.execute("""
                    UPDATE clients SET first_name = %s, surname = %s, 
                    email = %s, phone_number = %s WHERE client_id=%s;
                    """, (client_id, first_name, surname, email, phone_number))
        return self.cur.fetchone()

    def delete_phone(self, conn, client_id, phone_number):
        with conn.cursor() as self.cur:
            self.cur.execute("""
                    DELETE FROM phone_numbers WHERE client_id=%s AND phone_number=%s;
                    """, (client_id,phone_number))
        return self.cur.fetchone()

    def delete_client(self, conn, client_id):
        with conn.cursor() as self.cur:
            self.cur.execute("""
                    DELETE FROM phone_numbers WHERE client_id=%s;
                    DELETE FROM clients WHERE client_id=%s;
                    """, (client_id,))

    def find_client(self, conn, first_name=None, surname=None, email=None, phone_number=None):
        with conn.cursor() as self.cur:
            self.cur.execute("""
                    SELECT DISTINCT first_name, surname FROM clients
                    WHERE first_name=%s OR surname=%s OR email=%s OR phone_number=%s
                    """, (first_name, surname, email, phone_number))
        return self.cur.fetchone()


with psycopg2.connect(dbname="homework", user="postgres", password="lenochka77") as conn:
    data = Table()
    data.find_client(conn, 'Lavreneva')


conn.close()
