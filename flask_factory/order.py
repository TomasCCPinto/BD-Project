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
    print(id_user)

    query = f"Select * from buyer where customer_id_user = {id_user};"
    message = {}

    try:
        with db.get_data_base() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)

                if cursor.rowcount == 1:
                    query_order = f"INSERT INTO to_order (buyer_customer_id_user) values ({id_user}); select currval('to_order_id_order_seq');"
                    cursor.execute(query_order)
                    id_order = cursor.fetchall()[0] 
                    #print(id_order)
                    #meio javardo
                    #query_id_order = "select max(id_order) from to_order;"
                    #cursor.execute(query_id_order)
                    #id_order = cursor.fetchall()[0] 
                    
                    
                    
                    error=0
                    for x in cart:
                        query_prod = f"select * from product where id_prod = {x[0]};"
                        cursor.execute(query_prod)
                        
                        if cursor.rowcount != 1:
                            
                            message["status"] = GET_ERROR_CODE
                            message["error"]  = "Error selecting a product"
                            error=1
                            conn.rollback()
                            break
                        product = cursor.fetchall()[0]
                        #query_quantity = f"select stock from product where id_prod = {x[0]} ;"
                        #cursor.execute(query_quantity)
                        #row   = cursor.fetchall()[0]
                        
                        if (product[2]<x[1]):
                            message["status"] = GET_ERROR_CODE
                            message["error"]  = "No stock available"
                            error=1
                            conn.rollback()
                            break

                        new_stock = product[2] - x[1] 
                        query_prod_up = f"update product set stock = {new_stock} where id_prod = {x[0]};"
                        cursor.execute(query_prod_up)
                        conn.rollback()
                        #print(id_order)
                        query_quantity_add = f"insert into quantity (quantity, to_order_id_order,  product_id_prod) values ({x[1]}, {id_order[0]},{product[0]});"
                        cursor.execute(query_quantity_add) 
                        

                    if error:
                        conn.rollback()
                    else:
                        message["status"]  = SUCCESS_CODE
                        message["message"] = "ORDER COMPLETED"
                        message["result"] = id_order[0]
 
                                            
                    #row   = cursor.fetchall()[0]                 
                    #message["status"]  = SUCCESS_CODE
                    #message["message"] = "Product values updated"
                    #message["results"] = row[0]
                else:
                    message["status"] = GET_ERROR_CODE
                    message["error"]  = "Only buyers can do orders"


    except:
        return jsonify({
            "status": POST_ERROR_CODE,
            "error": "Something wrong happened"
        })


    return jsonify(message)