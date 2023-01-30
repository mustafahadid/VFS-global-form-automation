import sqlite3


def create_Db():
    conn = sqlite3.connect("db.db")
    # create cursor
    cur = conn.cursor()
    # create table
    cur.execute("""
    CREATE TABLE customers(
        cid INTEGER PRIMARY KEY AUTOINCREMENT,
        email text,
        pass text,
        visa_center text,
        visa_type text,
        visa_cathegory text,
        first_name text,
        last_name text,
        sex text,
        birth_data text,
        nationality text,
        passport_no text,
        passport_expire text,
        country_code text,
        phone_no text,
        new_email text
    )""")
    conn.commit()
    conn.close()


create_Db()
