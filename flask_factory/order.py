from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, decode_token
#status e database
from status.status import *
import database.db as db

order = Blueprint("order", __name__, url_prefix="/api/")

@order.route("/order", methods = ["POST"])
def add_order():
    # get and check args
    
    try:
        args = request.get_json()
        
    except:
        return jsonify({
            "status": GET_ERROR_CODE,
            "error": "No json"
        })

    
    if "cart" not in args or "token" not in args:
        
        return jsonify({
            "status": GET_ERROR_CODE,
            "error": "Wrong parameters"
        })

    cart = args["cart"]
    token    = decode_token(args["token"])
    id_user = token["sub"]["id"]

    query = f"Select * from buyer where customer_id_user = {id_user};"
    message = {}

    try:
        with db.get_data_base() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)

                if cursor.rowcount == 1:
                    #the id increments even when the program fails so the number gets higher than expected
                    query_order = f"INSERT INTO to_order (buyer_customer_id_user) values ({id_user}); select currval('to_order_id_order_seq');"
                    cursor.execute(query_order)
                    id_order = cursor.fetchall()[0] 
                    
                           
                                       
                    error=0
                    for x in cart:
                        query_prod = f"select * from product where id_prod = {x[0]} order by version;"
                        cursor.execute(query_prod)
                       
                        if cursor.rowcount == 0:
                            
                            message["status"] = GET_ERROR_CODE
                            message["error"]  = "Error selecting a product"
                            error=1
                            conn.rollback()
                            break
                        
                        product = cursor.fetchall()[-1]
                        
                        if (product[3]<x[1]):
                            message["status"] = GET_ERROR_CODE
                            message["error"]  = f"No stock available for product with id {x[0]}"
                            error=1
                            break
                        
                        new_stock = product[3] - x[1] 
                        query_prod_up = f"update product set stock = {new_stock} where id_prod = {x[0]} and version = {product[1]};"
                        cursor.execute(query_prod_up)
                        
                        

                        query_quantity_add = f"insert into quantity (quantity, to_order_id_order,  product_id_prod, product_version) values ({x[1]}, {id_order[0]},{product[0]},{product[1]});"
                        cursor.execute(query_quantity_add) 
                        
                       
                        
                        

                    if error:
                        conn.rollback()
                    else:
                        message["status"]  = SUCCESS_CODE
                        message["message"] = "ORDER COMPLETED"
                        message["result"] = id_order[0]
 
                                            
                 
                else:
                    message["status"] = GET_ERROR_CODE
                    message["error"]  = "Only buyers can do orders"


    except:
        return jsonify({
            "status": POST_ERROR_CODE,
            "error": "Something wrong happened"
        })


    return jsonify(message)