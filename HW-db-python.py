from pprint import pprint
import psycopg2

with psycopg2.connect (database="hwsql-4", user="postgres", password="196788") as conn:

# Функция "создать структуру БД (таблицы)"

    # очистка - удаление таблиц
    with conn.cursor() as cur:
        cur.execute("""
            DROP TABLE IF EXISTS Clientphones;
            DROP TABLE IF EXISTS Clients;
            """)

        conn.commit()
        
    # создание таблиц
        def create_db ():
            cur = conn.cursor()
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
        
            conn.commit() # фиксируем в БД
            return
        
# Функция "добавить нового клиента"

    with conn.cursor() as cur:

        def add_client (f_name, l_name, mail, cl_phone = ''):
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO
                Clients (first_name, last_name, email)
                VALUES(%s, %s, %s)
                RETURNING id
                """, (f_name, l_name, mail))
            cl_id = cur.fetchone()[0]

            if cl_phone != '':
                cur.execute("""
                INSERT INTO Clientphones (client_id, phone) 
                VALUES (%s, %s)
                """, (cl_id, cl_phone))
        
            conn.commit()  # фиксируем в БД
            return

# Функция "добавить телефон для существующего клиента"

    with conn.cursor() as cur:
        def add_phone(f_name: str, l_name: str, mail: str, cl_phone: str):

            def get_client_id(cur, f_name: str, l_name: str, mail: str) -> int:
                cur.execute("""
                    SELECT id FROM Clients WHERE first_name=%s and last_name=%s and email=%s;
                    """, (f_name, l_name, mail))
        
                cli_id = cur.fetchone()[0]
                return cli_id

            cl_id = get_client_id(cur, f_name, l_name, mail)
    
            cur.execute("""
                INSERT INTO Clientphones (client_id, phone)
                VALUES(%s, %s);
                """, (cl_id, cl_phone))

            conn.commit()  # фиксируем в БД
            return
            
# Функция "изменить данные о клиенте"

    with conn.cursor() as cur:
        def update_client(f_name: str, l_name: str, mail: str, n_f_name = '', n_l_name = '', n_mail = ''):

            def get_client_id(cur, f_name: str, l_name: str, mail: str) -> int:
                cur.execute("""
                    SELECT id FROM Clients WHERE first_name=%s and last_name=%s and email=%s;
                    """, (f_name, l_name, mail))
        
                cli_id = cur.fetchone()[0]
                return cli_id

            cl_id = get_client_id(cur, f_name, l_name, mail)

            if n_f_name != '':
                cur.execute("""
                    UPDATE Clients SET first_name=%s WHERE id = %s;
                    """, (n_f_name, cl_id))

            if n_l_name != '':
                cur.execute("""
                    UPDATE Clients SET last_name=%s WHERE id = %s;
                    """, (n_l_name, cl_id))    
                    
            if n_mail != '':
                cur.execute("""
                    UPDATE Clients SET email=%s WHERE id = %s;
                    """, (n_mail, cl_id))
        
            conn.commit()
            return

# Функция "удалить телефон для существующего клиента"

    with conn.cursor() as cur:
        def del_phone(f_name: str, l_name: str, mail: str, cl_phone: str):

            def get_client_id(cur, f_name: str, l_name: str, mail: str) -> int:
                cur.execute("""
                SELECT id FROM Clients WHERE first_name=%s and last_name=%s and email=%s;
                """, (f_name, l_name, mail))
                return cur.fetchone()[0]

            cl_id = get_client_id(cur, f_name, l_name, mail)

            cur.execute("""
                DELETE FROM Clientphones WHERE client_id=%s and phone=%s;
                """, (cl_id, cl_phone))

            return

# Функция "удалить существующего клиента"

    with conn.cursor() as cur:
        def del_client(f_name: str, l_name: str, mail: str):

            def get_client_id(cur, f_name: str, l_name: str, mail: str) -> int:
                cur.execute("""
                SELECT id FROM Clients WHERE first_name=%s and last_name=%s and email=%s;
                """, (f_name, l_name, mail))
                return cur.fetchone()[0]

            cl_id = get_client_id(cur, f_name, l_name, mail)

            cur.execute("""
            DELETE FROM Clientphones WHERE client_id=%s;
            """, (cl_id,))

            cur.execute("""
            DELETE FROM Clients WHERE id=%s;
            """, (cl_id,))

            return

# Функция "найти клиента по: имени, фамилии, email или телефону"

    with conn.cursor() as cur:

        def find_client(f_name ='%', l_name ='%', mail ='%', cl_phone ='%'):

            cur.execute("""
            SELECT DISTINCT cl.id FROM Clients cl
            LEFT JOIN Clientphones cl_ph ON cl.id = cl_ph.client_id
            WHERE cl.first_name LIKE %s and cl.last_name LIKE %s and cl.email LIKE %s and cl_ph.phone LIKE %s;
            """, (f_name, l_name, mail, cl_phone))

            list_id =[]
            for fetch in cur.fetchall():
                list_id.append(fetch[0])
            finded_clients = tuple(list_id)
            return finded_clients

# conn.close()

    if __name__ == "__main__":
        # Создание структуры БД
        create_db()
        
        with conn.cursor() as cur:
        # Добавление новых клиентов
            add_client("Ivan", "Ivanov", "ivanov@example.com")
            add_client("Petr", "Petrov", "petrov@example.com", "89012345678")
            add_client("Sidor", "Sidorov", "sidorov@example.com", "98765432109")
            add_client("Сергей", "Смирнов", "smirnov@example.com", "76543210987")
            add_client("Прохор", "Попов", "popov@example.com", "65432109876")
            add_client("Семен", "Соколов", "semenov@example.com", "12345678901")
            add_client("Федор", "Федоров", "fedorov@example.com", "23456789012")
            add_client("Павел", "Павлов", "pavlov@example.com", "34567890123")
            add_client("Егор", "Егоров", "egorov@example.com", "45678901234")
            add_client("Олег", "Орлов", "orlov@example.com", "56789012345")

            cur.execute("""
            SELECT cl.first_name, cl.last_name, cl.email, cl_ph.phone FROM Clients cl
            LEFT JOIN Clientphones cl_ph ON cl.id = cl_ph.client_id;
            """)
            pprint(cur.fetchall())

        # Добавление телефонов для существующих клиентов
            add_phone("Ivan", "Ivanov", "ivanov@example.com", "12345678901")
            add_phone("Егор", "Егоров", "egorov@example.com", "74108529630")
            add_phone("Егор", "Егоров", "egorov@example.com", "85296374100")

            cur.execute("""
                SELECT cl.first_name, cl.last_name, cl.email, cl_ph.phone FROM Clients cl
                LEFT JOIN Clientphones cl_ph ON cl.id = cl_ph.client_id;
                """)
            pprint(cur.fetchall())
    
        # Изменение данных о клиенте
            update_client("Ivan", "Ivanov", "ivanov@example.com", "Иван", "Иванов", "ivanoff@mail.ru")
            cur.execute("""
                SELECT cl.first_name, cl.last_name, cl.email, cl_ph.phone FROM Clients cl
                LEFT JOIN Clientphones cl_ph ON cl.id = cl_ph.client_id;
                """)
            pprint(cur.fetchall())

        # Удаление телефона
            del_phone("Petr", "Petrov", "petrov@example.com", "89012345678")
            cur.execute("""
                SELECT cl.first_name, cl.last_name, cl.email, cl_ph.phone FROM Clients cl
                LEFT JOIN Clientphones cl_ph ON cl.id = cl_ph.client_id;
                """)
            pprint(cur.fetchall())

        # Удаление клиента
            del_client("Sidor", "Sidorov", "sidorov@example.com")
            cur.execute("""
                SELECT cl.first_name, cl.last_name, cl.email, cl_ph.phone FROM Clients cl
                LEFT JOIN Clientphones cl_ph ON cl.id = cl_ph.client_id;
                """)
            pprint(cur.fetchall())

        # Поиск клиента по его данным: имени, фамилии, email или телефону
            f_id = find_client(f_name="Егор")
            cur.execute("""
                SELECT cl.first_name, cl.last_name, cl.email, cl_ph.phone FROM Clients cl
                LEFT JOIN Clientphones cl_ph ON cl.id = cl_ph.client_id WHERE cl.id IN %s;
                """, (f_id,))
            pprint(cur.fetchall())

            f_id = find_client(l_name="Орлов")
            cur.execute("""
                SELECT cl.first_name, cl.last_name, cl.email, cl_ph.phone FROM Clients cl
                LEFT JOIN Clientphones cl_ph ON cl.id = cl_ph.client_id WHERE cl.id = %s;
                """, (f_id))
            pprint(cur.fetchall())

            f_id = find_client(mail="pavlov@example.com")
            cur.execute("""
                SELECT cl.first_name, cl.last_name, cl.email, cl_ph.phone FROM Clients cl
                LEFT JOIN Clientphones cl_ph ON cl.id = cl_ph.client_id WHERE cl.id = %s;
                """, (f_id))
            pprint(cur.fetchall())

            f_id = find_client(cl_phone="23456789012")
            cur.execute("""
                SELECT cl.first_name, cl.last_name, cl.email, cl_ph.phone FROM Clients cl
                LEFT JOIN Clientphones cl_ph ON cl.id = cl_ph.client_id WHERE cl.id = %s;
                """, (f_id))
            pprint(cur.fetchall())

            f_id = find_client(cl_phone="74108529630")
            cur.execute("""
                SELECT cl.first_name, cl.last_name, cl.email, cl_ph.phone FROM Clients cl
                LEFT JOIN Clientphones cl_ph ON cl.id = cl_ph.client_id WHERE cl.id = %s;
                """, (f_id))
            pprint(cur.fetchall())
                        