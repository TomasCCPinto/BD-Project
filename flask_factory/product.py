
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, jsonify, request
#status e database
from status.status import *
import database.db as db


product = Blueprint("product", __name__, url_prefix="/api/product/")


@product.route("/add", methods = ["POST"])
def add_product():
    # get and check args
    try:
        args = request.get_json()
    except:
        return jsonify({
            "status": GET_ERROR_CODE,
            "error": "No json"
        })
    if "" not in args or "nif" not in args or "adress" not in args or "email" not in args or "password" not in args:

        return jsonify({
            "status": GET_ERROR_CODE,
            "error": "Wrong parameters"
        })

