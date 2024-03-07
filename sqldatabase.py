import sqlite3


def create_database(name):
    conn = sqlite3.connect("cars_database.db")

    cursor = conn.cursor()

    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS {name} (year INTEGER, model TEXT, price INTEGER, engine REAL, milage INTEGER, url TEXT PRIMARY KEY)"""
    )

    conn.commit()

    conn.close()


def insert_in_db(name: str, element: list):

    conn = sqlite3.connect("cars_database.db")
    curs = conn.cursor()
    data_base_records = []
    query = f"""SELECT * FROM {name}"""
    curs.execute(query)
    records = curs.fetchall()
    for record in records:
        data_base_records.append(record)
    print(len(data_base_records))

    for car in element:
        if car not in data_base_records:
            # print(f"car {car} not in data base\nAdding.....")
            curs.execute(f"INSERT OR IGNORE INTO {name} VALUES (?, ?, ?, ?, ?, ?)", car)
            conn.commit()
            text = "Jauna beha tirgu!!! " + "www.ss.com/" + str(car[3])
            # bot_send_message(text)
        # else:
        # print(f"Car {car} already in data base")
    conn.close()
    return data_base_records


def select_from_db(name: str, element: list):
    conn = sqlite3.connect("behas.db")
    curs = conn.cursor()
    data_base_records = []
    query = f"""SELECT * FROM {name} WHERE year BETWEEN 2019 AND 2025 AND price BETWEEN 15000 AND 50000 """
    curs.execute(query)
    records = curs.fetchall()
    print(records)
    # for record in records:
    #     data_base_records.append(record)
    # print(len(data_base_records))

    # for car in element:
    #     if car not in data_base_records:
    #         print(f"car {car} not in data base\nAdding.....")
    #         curs.execute("INSERT OR IGNORE INTO cars VALUES (?, ?, ?, ?, ?, ?)", car)
    #         conn.commit()
    #         text = "Jauna beha tirgu!!! " + "www.ss.com/" + str(car[3])
    #         # bot_send_message(text)
    #     else:
    #         print(f"Beha {car} already in data base")
    # conn.close()
    # return data_base_records
