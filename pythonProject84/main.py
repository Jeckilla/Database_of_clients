import psycopg2

from connection import conn


class Table(object):

    def __init__(self):
        self.connection = conn
        self.cursor = conn.cursor()

    def drop_tables(self, name_of_table):
        with self.connection.cursor() as cursor:
            cursor.execute(f"DROP TABLE IF EXISTS {name_of_table};")

    def create_table(self, name_of_table, column1, column2, column3, column4=None, column5=None):
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {name_of_table}(
            {column1} SERIAL PRIMARY KEY,
            {column2} VARCHAR(40),
            {column3} VARCHAR(40),
            {column4} VARCHAR(40) UNIQUE,
            {column5} BIGINT
            );
            """)

    def table_with_relations(self, name_of_table, column1, column2, column3):

        self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {name_of_table}(
                {column1} SERIAL PRIMARY KEY,
                {column2} BIGINT,
                {column3} INTEGER NOT NULL REFERENCES clients(id)
                );
                """)


    def add_client(self, first_name, surname, email, phone_number: int = None):
        self.cursor.execute("""
                INSERT INTO clients (first_name, surname, email)
                VALUES (%s, %s, %s)
                RETURNING id;
                """, (first_name, surname, email))
        client_id = self.cursor.fetchone()[0]

        if phone_number is not None:
            self.cursor.execute("""
                INSERT INTO phone_numbers (phone_number, client_id)
                VALUES (%s, %s);
                """, (phone_number, client_id))


    def add_phone(self, client_id, phone_number):
            self.cursor.execute("""
                    INSERT INTO phone_numbers (phone_number, client_id)
                    VALUES (%s, %s);
                    """, (phone_number, client_id))
            return f'Номер телефона {phone_number} успешно добавлен клиенту {client_id}'

    def update_phone(self, client_id, phone_id, phone_number):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                                SELECT client_id FROM phone_numbers WHERE client_id=%s;
                                """, (client_id,))
            result = cursor.fetchone()
            if result is None:
                print("Клиент с таким номером не найден")
            else:
                cursor.execute("""
                        UPDATE phone_numbers SET phone_number=%s WHERE client_id=%s AND phone_id=%s;
                        """, (phone_number, client_id, phone_id))
                return f"Данные о клиенте {client_id} изменены"


    def change_client(self):
        client_id = input("Введите id клиента, в данные которого необходимо внести изменения: ")
        with self.connection.cursor() as self.cursor:
            self.cursor.execute("""
                        SELECT id FROM clients WHERE id=%s;
                        """, (client_id,))
            result = self.cursor.fetchone()
            if result is None:
                print("Клиент с таким номером не найден")
            else:
                column_name = input("Какие данные о клиенте вы хотите изменить: (first_name, "
                                    "surname, email, phone_number) ")
                if column_name not in ['first_name', 'surname', 'email', 'phone_number']:
                    print("Такого столбца не существует")
                else:
                    value = input("Введите здесь значение, на которое необходимо изменить данные: ")
                    if column_name == 'first_name':
                        self.cursor.execute("""
                                UPDATE clients SET first_name=%s WHERE id=%s;
                                """, (value, client_id))
                    elif column_name == 'surname':
                        self.cursor.execute("""
                            UPDATE clients SET surname=%s WHERE id=%s;
                            """, (value, client_id))
                    elif column_name == 'email':
                        self.cursor.execute("""
                            UPDATE clients SET email=%s WHERE id=%s;
                            """, (value, client_id))
                    elif column_name == 'phone_number':
                        self.cursor.execute("""
                            UPDATE phone_numbers SET phone_number=%s WHERE client_id=%s;
                            """, (value, client_id))
                    return f'Данные о клиенте id = {client_id} изменены'


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


    def delete_client(self, client_id):
        self.cursor.execute("""
                        SELECT client_id FROM phone_numbers WHERE client_id=%s;
                        """, (client_id,))
        result = self.cursor.fetchone()
        if result is None:
            print("Клиент с таким номером не найден")
        else:
            self.cursor.execute("""
                        DELETE FROM phone_numbers WHERE client_id=%s;
                        DELETE FROM clients WHERE id=%s;
                        """, (client_id, client_id))

            return f'Клиент {client_id} удален из таблицы'


    def find_client(self):
        column_name, query = input("Введите столбец, по которому необходимо произвести поиск:  "), \
            input("Введите поисковый запрос: ")
        if column_name not in ['first_name', 'surname', 'email', 'phone_number']:
            print("Такого столбца не существует")
        else:
            if column_name == 'first_name':
                self.cursor.execute("""
                            SELECT first_name, surname, email, phone_number FROM clients
                            WHERE first_name=%s;
                            """, (query,))
                result = self.cursor.fetchone()
                if result:
                    print(result)
                else:
                    print("Ничего не найдено")

            elif column_name == 'surname':
                self.cursor.execute("""
                            SELECT first_name, surname, email, phone_number FROM clients
                            WHERE surname=%s;
                            """, (query,))
                result2 = self.cursor.fetchone()
                if result2:
                    print(result2)
                else:
                    print("Ничего не найдено")

            elif column_name == 'email':
                self.cursor.execute("""
                            SELECT first_name, surname, email, phone_number FROM clients
                            WHERE email=%s;
                            """, (query,))
                result3 = self.cursor.fetchone()
                if result3:
                    print(result3)
                else:
                    print("Ничего не найдено")

            elif column_name == 'phone_number':
                self.cursor.execute("""
                            SELECT first_name, surname, email, phone_number FROM clients
                            WHERE phone_number=%s;
                            """, (query,))
                result4 = self.cursor.fetchone()
                if result4:
                    print(result4)
                else:
                    print("Ничего не найдено")


    def select_all_data(self):
        self.cursor.execute("""
                            SELECT * FROM clients c
                            JOIN phone_numbers p ON c.id = p.client_id;
                            """)
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)


if __name__ == '__main__':
    with conn as conn:
        with conn.cursor() as cursor:
            data = Table()
            # data.create_table("clients", "id", "first_name", "surname", "email", "phone_number")
            # data.table_with_relations("phone_numbers", "phone_id", "phone_number", "client_id")
            # data.add_client('Ivan', 'Smirnov', 'vanya_vanyusha@mail.ru', 8960575484)
            # data.add_client('Sergey', 'Shapoval', 'shapa@gmail.com', 89996263539)
            # data.add_client('Alexander', 'Ivanov', 'ivanovalex@yandex.ru', 89215476623)
            # data.add_client('Maria', 'Lavreneva', 'lavmar@yandex.ru', 89042564917)
            # data.add_client('Elena', 'Konstantinova', 'konstanta@yandex.ru', 89215976314)
            # data.add_client('Anna', 'Smirnova', 'anna2022@yandex.ru', 89995874963)
            # data.add_client('Tamara', 'Petrova', 'tamara@yandex.ru', 89053747263)
            # data.find_client()
            # data.delete_client(8)
            # data.update_phone(4, 4, 89000000097)
            # data.change_client()
            # data.delete_phone(6, 89995874963)
            # data.add_phone(4, 89113452719)

            # data.select_all_data()
            # data.create_table("test", "id_test", "name_test", "surname_test", "email_test")
            # data.drop_tables('test')

# cursor.close()
# conn.close()
