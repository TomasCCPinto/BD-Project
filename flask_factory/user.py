from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, jsonify, request

from status import *
import database as db

user = Blueprint("user", __name__, url_prefix="/api/")


@user.route("/login", methods=["get", "post", "put"])
def login():
    args = request.get_json()

    if "email" not in args or "password" not in args:
        return jsonify({
            "code": GET_ERROR_CODE,
            "message": "Wrong parameters"
        })

    mail = args["email"]

    query   = f"SELECT id_user, name, password FROM customer WHERE email like '{mail}';"
    message = {}

    try:
        conn   = db.get_data_base()
        cursor = conn.cursor()
        cursor.execute(query)
        row    = get_token(cursor)

        if cursor.rowcount == 0:
            message["code"]    = GET_ERROR_CODE
            message["message"] = "No user witth that credentials"
        
        elif check_password_hash(row[2], args["password"]):
            message["code"]    = SUCCESS_CODE
            message["message"] = "logged in"
        else:
            message["code4"]   = SUCCESS_CODE
            message["message"] = "Wrong password"
                
        cursor.close()
        conn.close()
    
    except:
        return jsonify({
            "code": POST_ERROR_CODE,
            "message": "Something wrong happened"
        })

    return jsonify(message)




def get_token(cursor):
    for row in cursor:
        return row
