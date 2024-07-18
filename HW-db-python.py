from pprint import pprint
import psycopg2


def delete_db(conn):

    with conn.cursor() as cur:

        cur.execute("""
            DROP TABLE IF EXISTS Clients CASCADE;
            DROP TABLE IF EXISTS Clientphones CASCADE;
            """)

    return
# Функция "создать структуру БД (таблицы)"

def create_db(conn):

    with conn.cursor() as cur:

        cur.execute("""
            CREATE TABLE IF NOT EXISTS Clients(
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(40) NOT NULL,
                last_name VARCHAR(40) NOT NULL,
                email  VARCHAR(40) NOT NULL UNIQUE
                );
           CREATE TABLE IF NOT EXISTS Clientphones(
               id SERIAL PRIMARY KEY,
               client_id INTEGER NOT NULL REFERENCES Clients (id),
               phone VARCHAR(20)
               );
               """)

    return


# Функция "добавить нового клиента"

def add_client (conn, f_name, l_name, mail, cl_phone = ''):

    with conn.cursor() as cur:

        cur.execute("""
            INSERT INTO
                Clients (first_name, last_name, email)
                VALUES(%s, %s, %s)
                RETURNING id
                """, (f_name, l_name, mail))

        cl_id = cur.fetchone()[0]

        if cl_phone != '':
            cur.execute("""
                INSERT INTO Clientphones (client_id, phone) VALUES (%s, %s)""",
                (cl_id, cl_phone))

    return


# Функция "добавить телефон для существующего клиента"

def add_phone(conn, f_name: str, l_name: str, mail: str, cl_phone: str):

    def get_client_id(cur, f_name: str, l_name: str, mail: str) -> int:

        cur.execute("""
            SELECT id FROM Clients WHERE first_name=%s and last_name=%s and email=%s;""",
            (f_name, l_name, mail))

        cli_id = cur.fetchone()[0]

        return cli_id

    with conn.cursor() as cur:

        cl_id = get_client_id(cur, f_name, l_name, mail)

        cur.execute("""INSERT INTO Clientphones (client_id, phone) VALUES(%s, %s);""", (cl_id, cl_phone))

    return


# Функция "изменить данные о клиенте"

def update_client(conn, f_name: str, l_name: str, mail: str, n_f_name = '', n_l_name = '', n_mail = ''):

    def get_client_id(cur, f_name: str, l_name: str, mail: str) -> int:

        cur.execute("""SELECT id FROM Clients WHERE first_name=%s and last_name=%s and email=%s;""", (f_name, l_name, mail))

        cli_id = cur.fetchone()[0]

        return cli_id

    with conn.cursor() as cur:

        cl_id = get_client_id(cur, f_name, l_name, mail)

        if n_f_name != '':
            cur.execute("""UPDATE Clients SET first_name=%s WHERE id = %s;""", (n_f_name, cl_id))

        if n_l_name != '':
            cur.execute("""UPDATE Clients SET last_name=%s WHERE id = %s;""", (n_l_name, cl_id))    
                    
        if n_mail != '':
            cur.execute("""UPDATE Clients SET email=%s WHERE id = %s;""", (n_mail, cl_id))

    return


# Функция "удалить телефон для существующего клиента"

def del_phone(conn, f_name: str, l_name: str, mail: str, cl_phone: str):

    def get_client_id(cur, f_name: str, l_name: str, mail: str) -> int:

        cur.execute("""
            SELECT id FROM Clients WHERE first_name=%s and last_name=%s and email=%s;""", (f_name, l_name, mail))

        return cur.fetchone()[0]

    with conn.cursor() as cur:

        cl_id = get_client_id(cur, f_name, l_name, mail)

        cur.execute("""DELETE FROM Clientphones WHERE client_id=%s and phone=%s;""", (cl_id, cl_phone))

    return


# Функция "удалить существующего клиента"

def del_client(conn, f_name: str, l_name: str, mail: str):

    def get_client_id(cur, f_name: str, l_name: str, mail: str) -> int:

        cur.execute("""SELECT id FROM Clients WHERE first_name=%s and last_name=%s and email=%s;""", (f_name, l_name, mail))

        return cur.fetchone()[0]

    with conn.cursor() as cur:

        cl_id = get_client_id(cur, f_name, l_name, mail)

        cur.execute("""DELETE FROM Clientphones WHERE client_id=%s;""", (cl_id,))

        cur.execute("""DELETE FROM Clients WHERE id=%s;""", (cl_id,))

    return


# Функция "найти клиента по: имени, фамилии, email или телефону"

def find_client(conn, f_name ='%', l_name ='%', mail ='%', cl_phone ='%'):

    with conn.cursor() as cur:

        cur.execute("""SELECT DISTINCT cl.id FROM Clients cl
            LEFT JOIN Clientphones cl_ph ON cl.id = cl_ph.client_id
            WHERE cl.first_name LIKE %s and cl.last_name LIKE %s and cl.email LIKE %s and cl_ph.phone LIKE %s;
            """, (f_name, l_name, mail, cl_phone))

        list_id =[]

        for fetch in cur.fetchall():
            list_id.append(fetch[0])

        finded_clients = tuple(list_id)

    return finded_clients



if __name__ == "__main__":

   with psycopg2.connect (database="hwsql-4", user="postgres", password="196788") as conn:

        # Очистка - Удаление таблиц

        delete_db(conn)

        
        # Создание структуры БД

        create_db(conn)


        # Добавление новых клиентов

        add_client(conn, "Ivan", "Ivanov", "ivanov@example.com")
        add_client(conn, "Petr", "Petrov", "petrov@example.com", "89012345678")
        add_client(conn, "Sidor", "Sidorov", "sidorov@example.com", "98765432109")
        add_client(conn, "Сергей", "Смирнов", "smirnov@example.com", "76543210987")
        add_client(conn, "Прохор", "Попов", "popov@example.com", "65432109876")
        add_client(conn, "Семен", "Соколов", "semenov@example.com", "12345678901")
        add_client(conn, "Федор", "Федоров", "fedorov@example.com", "23456789012")
        add_client(conn, "Павел", "Павлов", "pavlov@example.com", "34567890123")
        add_client(conn, "Егор", "Егоров", "egorov@example.com", "45678901234")
        add_client(conn, "Олег", "Орлов", "orlov@example.com", "56789012345")

        with conn.cursor() as cur:

            cur.execute("""
                SELECT cl.first_name, cl.last_name, cl.email, cl_ph.phone FROM Clients cl
                LEFT JOIN Clientphones cl_ph ON cl.id = cl_ph.client_id;
                """)

            pprint(cur.fetchall())


        # Добавление телефонов для существующих клиентов

        add_phone(conn, "Ivan", "Ivanov", "ivanov@example.com", "12345678901")
        add_phone(conn, "Егор", "Егоров", "egorov@example.com", "74108529630")
        add_phone(conn, "Егор", "Егоров", "egorov@example.com", "85296374100")

        with conn.cursor() as cur:

            cur.execute("""
                SELECT cl.first_name, cl.last_name, cl.email, cl_ph.phone FROM Clients cl
                LEFT JOIN Clientphones cl_ph ON cl.id = cl_ph.client_id;
                """)

            pprint(cur.fetchall())
    

        # Изменение данных о клиенте

        update_client(conn, "Ivan", "Ivanov", "ivanov@example.com", "Иван", "Иванов", "ivanoff@mail.ru")

        with conn.cursor() as cur:

            cur.execute("""
                SELECT cl.first_name, cl.last_name, cl.email, cl_ph.phone FROM Clients cl
                LEFT JOIN Clientphones cl_ph ON cl.id = cl_ph.client_id;
                """)

            pprint(cur.fetchall())


        # Удаление телефона

        del_phone(conn, "Petr", "Petrov", "petrov@example.com", "89012345678")

        with conn.cursor() as cur:

            cur.execute("""
                SELECT cl.first_name, cl.last_name, cl.email, cl_ph.phone FROM Clients cl
                LEFT JOIN Clientphones cl_ph ON cl.id = cl_ph.client_id;
                """)

            pprint(cur.fetchall())


        # Удаление клиента

        del_client(conn, "Sidor", "Sidorov", "sidorov@example.com")

        with conn.cursor() as cur:

            cur.execute("""
                SELECT cl.first_name, cl.last_name, cl.email, cl_ph.phone FROM Clients cl
                LEFT JOIN Clientphones cl_ph ON cl.id = cl_ph.client_id;
                """)

            pprint(cur.fetchall())


        # Поиск клиента по его данным: имени, фамилии, email или телефону

        f_id = find_client(conn, f_name="Егор")

        with conn.cursor() as cur:
            cur.execute("""
                SELECT cl.first_name, cl.last_name, cl.email, cl_ph.phone FROM Clients cl
                LEFT JOIN Clientphones cl_ph ON cl.id = cl_ph.client_id WHERE cl.id IN %s;
                """, (f_id,))
            pprint(cur.fetchall())


        f_id = find_client(conn, l_name="Орлов")

        with conn.cursor() as cur:
            cur.execute("""
                SELECT cl.first_name, cl.last_name, cl.email, cl_ph.phone FROM Clients cl
                LEFT JOIN Clientphones cl_ph ON cl.id = cl_ph.client_id WHERE cl.id = %s;
                """, (f_id))
            pprint(cur.fetchall())


        f_id = find_client(conn, mail="pavlov@example.com")

        with conn.cursor() as cur:
            cur.execute("""
                SELECT cl.first_name, cl.last_name, cl.email, cl_ph.phone FROM Clients cl
                LEFT JOIN Clientphones cl_ph ON cl.id = cl_ph.client_id WHERE cl.id = %s;
                """, (f_id))
            pprint(cur.fetchall())


        f_id = find_client(conn, cl_phone="23456789012")

        with conn.cursor() as cur:

            cur.execute("""
                SELECT cl.first_name, cl.last_name, cl.email, cl_ph.phone FROM Clients cl
                LEFT JOIN Clientphones cl_ph ON cl.id = cl_ph.client_id WHERE cl.id = %s;
                """, (f_id))
            pprint(cur.fetchall())


        f_id = find_client(conn, cl_phone="74108529630")

        with conn.cursor() as cur:

            cur.execute("""
                SELECT cl.first_name, cl.last_name, cl.email, cl_ph.phone FROM Clients cl
                LEFT JOIN Clientphones cl_ph ON cl.id = cl_ph.client_id WHERE cl.id = %s;
                """, (f_id))
            pprint(cur.fetchall())

# conn.close()