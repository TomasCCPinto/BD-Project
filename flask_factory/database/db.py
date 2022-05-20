import psycopg2 as psy


USER = "postgres"
PASS = "postgres"
HOST = "127.0.0.1"
PORT = "5432"
DBASE = "dbshop"


# return the conniction to a data base
def get_data_base():
    """
    just return a connection to data base
    """

    dataBase = psy.connect(user = USER, password = PASS, host = HOST, port = PORT, database = DBASE)

    return dataBase
