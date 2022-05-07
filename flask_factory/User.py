
import database.db as db


class User:

    def __init__(self, id_user, username, password) -> None:

        query_adm = f"select * from administrator where customer_id_user = {id_user};"
        query_sel = f"select * from buyer         where customer_id_user = {id_user};"
        query_buy = f"select * from seller        where customer_id_user = {id_user};"


        with db.get_data_base() as conn:
            with conn.cursor() as cursor:

                cursor.execute(query_adm)
                if cursor.rowcount != 0:

                    self.attributes = {
                        "id": id_user,
                        "username": username,
                        "password": password,
                        "user_type": "administrator"
                    }

                cursor.execute(query_sel)
                if cursor.rowcount != 0:

                    self.attributes = {
                        "id": id_user,
                        "username": username,
                        "password": password,
                        "userType": "seller"
                    }
                
                cursor.execute(query_buy)
                if cursor.rowcount != 0:

                    self.attributes = {
                        "id": id_user,
                        "username": username,
                        "password": password,
                        "userType": "buyer"
                    }

    def show(self):
        print(self.attributes)