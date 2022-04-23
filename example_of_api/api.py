import psycopg2 as psy


def connetion_db():
    db = psy.connect(user = 'postgres', password = 'postgres', host = '127.0.0.1', database = "test")

    return db

def main():
    conn   = connetion_db()
    cursor = conn.cursor()
    sql    = "SELECT * FROM customer WHERE name like 'joao'"

    cursor.execute(sql)

    print(cursor)

    for row in cursor:
        print(row)



main()