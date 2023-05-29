import psycopg2


class Table(object):
    def __init__(self):
        with psycopg2.connect(dbname="homework", user="postgres", password="lenochka77", host='localhost', port='5432') as conn:
            self.cursor = conn.cursor()

    def drop_tables(self, name_of_table):

        self.cursor.execute("""
            DROP TABLE name_of_table=%s;
            """, (name_of_table,))

        self.cursor.conn.commit()

    def create_table(self, name_of_table, column1, column2, column3, column4=None, column5=None):

        self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {name_of_table}(
                {column1} SERIAL PRIMARY KEY,
                {column2} VARCHAR(40),
                {column3} VARCHAR(40),
                {column4} VARCHAR(40) UNIQUE,
                {column5} INTEGER
                );
                """)

        self.cursor.conn.commit()

    def table_with_relations(self, name_of_table, column1, column2, column3=None):

        self.cursor.execute(f"""
                   CREATE TABLE IF NOT EXISTS {name_of_table}(
                   {column1} SERIAL PRIMARY KEY,
                   {column2} INTEGER,
                   {column3} INTEGER NOT NULL REFERENCES clients2(id)
                   );
                   """)

        self.cursor.conn.commit()

    def add_client(self, first_name, surname, email, phone_number=None):
        self.cursor.execute("""
               INSERT INTO clients2(first_name, surname, email, phone_number)
               VALUES (%s, %s, %s)
               RETURNING id;     
               """, (first_name, surname, email))
        client_id = self.cursor.fetchone()[0]
        self.cursor.conn.commit()

        if phone_number:
            self.cursor.execute("""
                INSERT INTO phone_numbers(phone_number, client_id)
                VALUES (%s, %s);
                """, (phone_number, client_id))

        self.cursor.conn.commit()

    def update_phone(self, client_id, phone_id, phone_number):
        self.cursor.execute("""
                            SELECT client_id FROM phone_numbers WHERE client_id=%s;
                            """, (client_id,))
        result = self.cursor.fetchone()
        if result is None:
            print("Клиент с таким номером не найден")
        else:
            self.cursor.execute("""
                UPDATE phone_numbers SET phone_number=%s WHERE client_id=%s AND phone_id=%s;
                """, (client_id, phone_id, phone_number))
            return self.cursor.fetchone()

        self.cursor.conn.commit()

    def change_client(self):
        client_id = input("Введите id клиента, в данные которого необходимо внести изменения: ")
        column_name = input("Какие данные о клиенте вы хотите изменить: (first_name, surname, email, phone_number) ")
        value = input("Введите здесь значение, на которое необходимо изменить данные: ")
        self.cursor.execute("""
                    SELECT id FROM clients2 WHERE id=%s;
                    """, (client_id,))
        result = self.cursor.fetchone()
        if result is None:
            print("Клиент с таким номером не найден")
        else:
            if column_name == 'first_name':
                self.cursor.execute("""
                    UPDATE clients  SET first_name=%s WHERE id=%s;
                    """, (value, client_id))
            elif column_name == 'surname':
                self.cursor.execute("""
                    UPDATE clients  SET surname=%s WHERE id=%s;
                    """, (value, client_id))
            elif column_name == 'email':
                self.cursor.execute("""
                    UPDATE cliente SET email=%s WHERE id=%s;
                    """, (value, client_id))
            elif column_name == 'phone_number':
                self.cursor.execute("""
                    UPDATE clients SET phone_number=%s WHERE id=%s;
                    """, (value, client_id))
            return f'Данные о клиенте id = {client_id} изменены'

        self.cursor.conn.commit()

    def delete_phone(self, client_id, phone_number):
        self.cursor.execute("""
                              SELECT client_id FROM phone_numbers WHERE client_id=%s;
                              """, (client_id,))
        result = self.cursor.fetchone()
        if result is None:
            print("Клиент с таким номером не найден")
        else:
            self.cursor.execute("""
                    DELETE FROM phone_numbers WHERE client_id=%s AND phone_number=%s;
                    DELETE FROM clients WHERE phone_number=%s;
                    """, (client_id, phone_number, phone_number))
            return f"Номер телефона {phone_number} клиента {client_id} удален из таблиц"

        self.cursor.conn.commit()

    def delete_client(self, client_id):
        self.cursor.execute("""
                    SELECT client_id FROM phone_numbers WHERE client_id=%s;
                    """, (client_id,))
        result = cursor.fetchone()
        if result is None:
            print("Клиент с таким номером не найден")
        else:
            self.cursor.execute("""
                                DELETE FROM phone_numbers WHERE client_id=%s;
                                """, (client_id,))

            self.cursor.execute("""
                                DELETE FROM clients2 WHERE id=%s;
                                """, (client_id,))
            return f'Клиент {client_id} удален из таблицы'

        self.cursor.conn.commit()

    def find_client(self):
        column_name, query = input("Введите столбец, по которому необходимо произвести поиск:  "), \
            input("Введите поисковый запрос: ")
        if column_name not in ['first_name', 'surname', 'email', 'phone_number']:
            print("Такого столбца не существует")
        else:
            if column_name == 'first_name':
                self.cursor.execute("""
                           SELECT first_name, surname, email, phone_number FROM clients2
                           WHERE first_name=%s;
                           """, (query,))
                result = self.cursor.fetchone()
                if result:
                    print(result)
                else:
                    print("Ничего не найдено")

            elif column_name == 'surname':
                self.cursor.execute("""
                            SELECT first_name, surname, email, phone_number FROM clients2
                            WHERE surname=%s;
                            """, (query,))
                result2 = self.cursor.fetchone()
                if result2:
                    print(result2)
                else:
                    print("Ничего не найдено")

            elif column_name == 'email':
                self.cursor.execute("""
                            SELECT first_name, surname, email, phone_number FROM clients2
                            WHERE email=%s;
                            """, (query,))
                result3 = self.cursor.fetchone()
                if result3:
                    print(result3)
                else:
                    print("Ничего не найдено")

            elif column_name == 'phone_number':
                self.cursor.execute("""
                            SELECT first_name, surname, email, phone_number FROM clients2
                            WHERE phone_number=%s;
                            """, (query,))
                result4 = self.cursor.fetchone()
                if result4:
                    print(result4)
                else:
                    print("Ничего не найдено")

        self.cursor.conn.commit()


with psycopg2.connect(dbname="homework", user="postgres", password="lenochka77") as conn:
    cursor = conn.cursor()
    data = Table()
    data.create_table("clients", "id", "first_name", "surname", "email", "phone_number")
    # data.table_with_relations(conn, "phone_numbers", "phone_id", "phone_number", "client_id")
    # data.add_client('Ivan', 'Smirnov', 'vanya_vanyusha@mail.ru', 8960575484)
    # data.add_client('Sergey', 'Shapoval', 'shapa@gmail.com', 89996263539)
    # data.add_client('Alexander', 'Ivanov', 'ivanovalex@yandex.ru', 89215476623)
    # data.add_client('Maria', 'Lavreneva', 'lavmar@yandex.ru', 89042564917)
    # data.add_client('Elena', 'Konstantinova', 'konstanta@yandex.ru', 89215976314)
    # data.add_client('Anna', 'Smirnova', 'anna2022@yandex.ru', 89995874963)
    # data.find_client(conn)


# cursor.close()
# conn.close()
