
from flask import Blueprint, jsonify, request
from flask_jwt_extended import decode_token


from status.status import *
import database.db as db



rating = Blueprint("rating", __name__, url_prefix="/api/rating/")


# falta verificar se o user comprou esse produto

@rating.route("/<int:prod_id>", methods = ["POST"])
def refresh_product(prod_id):

    try:
        args = request.get_json()
    except:
        return jsonify({
            "status": GET_ERROR_CODE,
            "error": "No json"
        })

    expected_args = ["rating", "comment", "token"]
    for arg in expected_args:
        if arg not in args:

            return jsonify({
                "status": GET_ERROR_CODE,
                "error": "Wrong parameters"
            })

    rating       = int(args["rating"])
    token        = decode_token(args["token"])
    comment      = args["comment"]
    id_user      = token["sub"]["id"]
    queryRating  = f"SELECT id_rating FROM rating WHERE buyer_customer_id_user = {id_user} and product_id_prod = {prod_id};"
    queryProduct = f"SELECT product_version FROM quantity INNER JOIN to_order ON quantity.to_order_id_order = to_order.id_order WHERE product_id_prod = {prod_id} AND to_order.buyer_customer_id_user = {id_user}"

    if not 1 <= rating <= 5:
       
        return jsonify({
            "status": GET_ERROR_CODE,
            "error": "Rating range exceeded"
        })
    
    message = {} 
    try:
        with db.get_data_base() as conn:
            with conn.cursor() as cursor:
                cursor.execute(queryRating)

                # check no exits this rating
                if cursor.rowcount == 0:
                    cursor.execute(queryProduct)
                    row          = cursor.fetchall()[-1]
                    queryInsert  = f"INSERT INTO rating (rating, comment, buyer_customer_id_user, product_id_prod, product_version) VALUES ({rating}, '{comment}', {id_user}, {prod_id}, {row[0]});"

                    # check user bought the product
                    if cursor.rowcount != 0:
                        cursor.execute(queryInsert)
                        message["status"] = SUCCESS_CODE

                    else:
                        message["status"] = GET_ERROR_CODE
                        message["error"]  = "You can't rate this product"

                else:
                    message["status"] = GET_ERROR_CODE
                    message["error"]  = "Already exists a rating"

    except:
        
        return jsonify({
            "status": POST_ERROR_CODE,
            "error": "Something wrong happened"
        })


    return jsonify(message)



    # elect product.description, product.stock, product.price, product.type, product.weight, product.height, product.colour  from rating join product on rating.product_id_prod = product.id_prod where product.product_id_prod = 7;