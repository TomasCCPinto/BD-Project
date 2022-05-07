from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, decode_token

from status.status import *
import database.db as db
from User import User


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
                
                cursor.execute(query)
                row    = cursor.fetchall()[0]

                if cursor.rowcount == 0:
                    message["status"] = GET_ERROR_CODE
                    message["error"]  = "No user witth that credentials (username)"

                elif check_password_hash(row[2], password):
                    user              = User(row[0], row[1], row[2])
                    token             = create_access_token(identity=user.attributes)
                    message["status"] = SUCCESS_CODE
                    message["token"]  = token
                    #message["read"]   = decode_token(token)     # tomas delete this when you understand how to use tokens
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


    """
                                                        REGISTO DE SELLER OU ADMINS 
    """

    message = {}


    if "name" in args and "nif" in args and "adress" in args and "email" in args and "password" in args and "token" in args and "user_type" in args:

        type_U = args["user_type"]
        if type_U != "administrator" and type_U != "seller":

            return jsonify({
                "status": GET_ERROR_CODE,
                "error": "Cant register this type"
            })


        name     = args["name"]
        nif      = args["nif"]
        adress   = args["adress"]
        email    = args["email"]
        password = generate_password_hash(args["password"])
        token    = decode_token(args["token"])
        admin_id = token["sub"]["id"]

        query   = f"SELECT * FROM administrator WHERE customer_id_user = '{admin_id}';"

        try:
            with db.get_data_base() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)

                    if cursor.rowcount != 0:
                        query = f"INSERT INTO customer (name, nif, adress, email, password) VALUES ('{name}', '{nif}', '{adress}', '{email}', '{password}'); SELECT currval('customer_id_user_seq');"
                        cursor.execute(query)
                        row   = cursor.fetchall()[0]

                        query = f"INSERT INTO {type_U} VALUES ('{row[0]}');"
                        cursor.execute(query)

                        message["status"]  = SUCCESS_CODE
                        message["message"] = "Regist completed"
                        message["user_id"] = row[0]
                        

                    else:
                        message["status"] = GET_ERROR_CODE
                        message["error"]  = "No permition/ Only admin can register seller/admins"
                        

        except:
            
            return jsonify({
                "status": POST_ERROR_CODE,
                "error": "Something wrong happened"
            })

    #                                                   REGISTO DE BUYERS
    elif "name" in args and "nif" in args and "adress" in args and "email" in args and "password" in args:

        name     = args["name"]
        nif      = args["nif"]
        adress   = args["adress"]
        email    = args["email"]
        password = generate_password_hash(args["password"])

        # check if person alredy register
        query   = f"SELECT * FROM customer WHERE name like '{name}'"

        try:
            with db.get_data_base() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)

                    if cursor.rowcount == 0:
                        query = f"INSERT INTO customer (name, nif, adress, email, password) VALUES ('{name}', '{nif}', '{adress}', '{email}', '{password}'); SELECT currval('customer_id_user_seq');"
                        cursor.execute(query)
                        row   = cursor.fetchall()[0]

                        query = f"INSERT INTO buyer VALUES ('{row[0]}');"
                        cursor.execute(query)

                        message["status"]  = SUCCESS_CODE
                        message["message"] = "Regist completed"
                        message["user_id"] = row[0]

                    else:
                        message["status"] = GET_ERROR_CODE
                        message["error"]  = "Username already registed"

        except:
            return jsonify({
                "status": POST_ERROR_CODE,
                "error": "Something wrong happened"
            })

    else:
        return jsonify({
            "status": GET_ERROR_CODE,
            "error": "Wrong parameters"
        })


    return jsonify(message)
