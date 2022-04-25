from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, jsonify, request

from status import *
import database as db

user = Blueprint("user", __name__, url_prefix="/api/")


@user.route("/login", methods=["get", "post", "put"])
def login():
    # get and check args
    args = request.get_json()
    if "email" not in args or "password" not in args:
        return jsonify({
            "code": GET_ERROR_CODE,
            "message": "Wrong parameters"
        })

    mail     = args["email"]
    password = args["password"]

    query   = f"SELECT id_user, name, password FROM customer WHERE email like '{mail}';"
    message = {}

    try:
        with db.get_data_base() as conn:
            with conn.cursor() as cursor:

                cursor.execute(query)
                row    = cursor.fetchall()[0]

                if cursor.rowcount == 0:
                    message["code"]    = GET_ERROR_CODE
                    message["message"] = "No user witth that credentials"

                if check_password_hash(row[2], password):
                    message["code"]    = SUCCESS_CODE
                    message["message"] = "logged in"
                else:
                    message["code4"]   = SUCCESS_CODE
                    message["message"] = "Wrong password"

    except:
        return jsonify({
            "code": POST_ERROR_CODE,
            "message": "Something wrong happened"
        })

    return jsonify(message)


@user.route("/register", methods = ["get", "post", "put"])
def register():

    # get and check args
    args = request.get_json()
    if "name" not in args or "nif" not in args or "adress" not in args or "email" not in args or "password" not in args:

        return jsonify({
            "code": GET_ERROR_CODE,
            "message": "Wrong parameters"
        })

    name     = args["name"]
    nif      = args["nif"]
    adress   = args["adress"]
    email    = args["email"]
    password = generate_password_hash(args["password"])
    
    # check if admin it is loged in to add -> only admin can add users

    # check if person alredy register
    query = f"SELECT id_user FROM customer WHERE email like '{email}'"
    message = {}

    try:
        with db.get_data_base() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)

                if cursor.rowcount == 0:
                    query = f"INSERT INTO customer (name, nif, adress, email, password) VALUES ('{name}', '{nif}', '{adress}', '{email}', '{password}');"

                    print("here")
                    cursor.execute(query)
                    print("here")

                    message["code"]    = SUCCESS_CODE
                    message["message"] = "Regist completed"

                else:
                    print("here2")
                    message["code"]    = GET_ERROR_CODE
                    message["message"] = "Email already registed"

    except:
        return jsonify({
            "code": POST_ERROR_CODE,
            "message": "Something wrong happened"
        })


    return jsonify(message)
