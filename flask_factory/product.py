
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
    if "name" not in args or "description" not in args or "stock" not in args or "price" not in args or "seller_customer_id_user" not in args:

        return jsonify({
            "status": GET_ERROR_CODE,
            "error": "Wrong parameters"
        })
    
    name     = args["name"]
    description      = args["description"]
    stock   = args["stock"]
    price    = args["price"]
    seller_customer_id_user  = args["seller_customer_id_user"]

    query   = f"SELECT * FROM product WHERE name like '{name}' and seller_customer_id_user = {seller_customer_id_user}"
    message = {}

    try:
        with db.get_data_base() as conn:
            with conn.cursor() as cursor:
                print("aquii")
                cursor.execute(query)

                if cursor.rowcount == 0:
                    query = f"INSERT INTO product (name, description, stock, price, seller_customer_id_user ) VALUES ('{name}', '{description}', {stock}, {price}, {seller_customer_id_user}); SELECT currval('product_id_prod_seq');"

                    cursor.execute(query)
                    row   = cursor.fetchall()[0]

                    message["status"]  = SUCCESS_CODE
                    message["message"] = "Product added successfully"
                    message["results"] = row[0]

                else:
                    message["status"] = GET_ERROR_CODE
                    message["error"]  = "product already registed"

    except:
        return jsonify({
            "status": POST_ERROR_CODE,
            "error": "Something wrong happened"
        })


    return jsonify(message)