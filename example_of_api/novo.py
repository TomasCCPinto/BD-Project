from email import message
from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

import psycopg2 as psy


def connetion_db():
    db = psy.connect(user = 'postgres', password = 'postgres', host = '127.0.0.1', database = "test")

    return db

app = Flask(__name__)


@app.route('/')
def root():
    return jsonify({"message" : "Welcome to the mother fucker shop program!"})

@app.route('/<name>')
def root_name(name):
    return {"message" : f"Welcome to the mother fucker shop program {name}!"}


def get_token(cursor):
    for row in cursor:
        return row[5]

    return ""

@app.get('/login/<string:name>/<string:password>')
def get_login(name, password):
    if name and password:
        conn   = connetion_db()
        cursor = conn.cursor()
        sql    = f"SELECT * FROM customer WHERE name like '{name}'"
        cursor.execute(sql)

        my_token = get_token(cursor)
        cursor.close()
        conn.close()

        if my_token != "":

            if check_password_hash(my_token, password):
                return jsonify({"pass": "BEM-VINDO"})
            else:
                return jsonify({"pass" : "A pass nao consta na base de dados"})
        else:
            return jsonify({"pass" : "O nome nao consta na base de dados"})

    return jsonify({"message" : "please enter a name or pass"})


def get_register(cursor, id_user, name, nif, adress, mail, password):
    if cursor.rowcount == 0:
        token = generate_password_hash(password=password)

        connetion = connetion_db()
        cursor    = connetion.cursor()
        sql       = f"INSERT INTO customer (id_user, name, nif, adress, email, password) VALUES ('{id_user}', '{name}', '{nif}', '{adress}', '{mail}', '{token}')"
        cursor.execute(sql)
        connetion.commit()
        cursor.close()
        connetion.close()

        return True
    else:
        return False


@app.route('/reg/<string:name>/<string:nif>/<string:addr>/<string:email>/<string:my_p>')
def set_register(name, nif, addr, email, my_p):
    if name and nif and addr and email and my_p:
        connetion = connetion_db()
        cursor    = connetion.cursor()
        sql       = f"SELECT * FROM customer WHERE name like '{name}'"

        cursor.execute(sql)
        cursor.close()

        if get_register(cursor, 32, name, nif, addr, email, my_p):    
            return {"menssage": "CONGRATS! seja bem vindo"}
        else:
            return {'message': "User ja registado"}
    return {'message': "ola"}

"""@app.route('/reg/<string:name>')
def set_register(name):
    if name:
        return {"message" : name}
    return {"message"}"""

# http://127.0.0.1:5000/register/tomas/3542198/rua%20do%20pinhal/tftlord@qualquer.coisa/seila

if __name__ == "__main__":
    app.run(debug=True)
