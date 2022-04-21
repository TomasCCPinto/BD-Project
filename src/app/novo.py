from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

import psycopg2 as psy


def connetion_db():
    db = psy.connect(user = 'postgres', password = 'postgres', host = '127.0.0.1', database = "test")

    return db

app = Flask(__name__)


@app.route('/')
def root():
    return {"message" : "Welcome to the mother fucker shop program!"}

def get_token(cursor):
    for row in cursor:
        return row[5]

    return ""

@app.route('/login/<string:name>/<string:password1>')
def get_login(name, password1):
    if name and password1:
        conn = connetion_db()
        cursor = conn.cursor()
        cursor.execute(sql)
        sql = f"SELECT * FROM customer WHERE name like '{name}'"

        my_token = get_token(cursor)

        if my_token != "":

            if check_password_hash(my_token, password1):
                return {"pass": "BEM-VINDO"}
            else:
                return {"pass" : "A pass nao consta na base de dados"}
        else:
            return {"pass" : "O nome nao consta na base de dados"}

    return jsonify({"message" : "please enter a name or pass"})


if __name__ == "__main__":
    app.run(debug=True)