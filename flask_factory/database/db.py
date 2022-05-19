import psycopg2 as psy


USER = "aulaspl"
PASS = "aulaspl"
HOST = "127.0.0.1"
PORT = "5432"
DBASE = "project"


# return the conniction to a data base
def get_data_base():
    """
    just return a connection to data base
    """

    dataBase = psy.connect(user = USER, password = PASS, host = HOST, port = PORT, database = DBASE)

    return dataBase
