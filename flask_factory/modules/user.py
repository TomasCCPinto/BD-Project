from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, jsonify, request

from status.status import *
import database.db as db

user = Blueprint("user", __name__, url_prefix="/api/")


@user.route("/login", methods=["put"])
def login():
    # get and check args
    try:
        args = request.get_json()
    except:
        return jsonify({
            "status": GET_ERROR_CODE,
            "error": "No json"
        })

    if "username" not in args or "password" not in args:
        return jsonify({
            "code": GET_ERROR_CODE,
            "message": "Wrong parameters"
        })

    username = args["username"]
    password = args["password"]

    query   = f"SELECT id_user, name, password FROM customer WHERE name like '{username}';"
    message = {}

    try:
        with db.get_data_base() as conn:
            with conn.cursor() as cursor:
                
                print("HERE")
                cursor.execute(query)
                print("HERE")
                row    = cursor.fetchall()[0]
                print("HERE")

                if cursor.rowcount == 0:
                    message["status"] = GET_ERROR_CODE
                    message["error"]  = "No user witth that credentials (username)"

                elif check_password_hash(row[2], password):
                    message["status"] = SUCCESS_CODE
                    message["token"]  = row[2]
                else:
                    message["status"] = GET_ERROR_CODE
                    message["error"]  = "Wrong password"

    except:
        return jsonify({
            "status": POST_ERROR_CODE,
            "error":  "Something wrong happened"
        })

    return jsonify(message)


@user.route("/register", methods = ["post"])
def register():

    # get and check args
    try:
        args = request.get_json()
    except:
        return jsonify({
            "status": GET_ERROR_CODE,
            "error": "No json"
        })

    if "name" not in args or "nif" not in args or "adress" not in args or "email" not in args or "password" not in args:

        return jsonify({
            "status": GET_ERROR_CODE,
            "error": "Wrong parameters"
        })

    name     = args["name"]
    nif      = args["nif"]
    adress   = args["adress"]
    email    = args["email"]
    password = generate_password_hash(args["password"])

    # check if person alredy register
    query   = f"SELECT * FROM customer WHERE email like '{name}'"
    message = {}

    try:
        with db.get_data_base() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)

                if cursor.rowcount == 0:
                    query = f"INSERT INTO customer (name, nif, adress, email, password) VALUES ('{name}', '{nif}', '{adress}', '{email}', '{password}'); SELECT currval('customer_id_user_seq');"

                    cursor.execute(query)
                    row   = cursor.fetchall()[0]

                    message["status"]  = SUCCESS_CODE
                    message["message"] = "Regist completed"
                    message["results"] = row

                else:
                    message["status"] = GET_ERROR_CODE
                    message["error"]  = "Username already registed"

    except:
        return jsonify({
            "status": POST_ERROR_CODE,
            "error": "Something wrong happened"
        })


    return jsonify(message)
