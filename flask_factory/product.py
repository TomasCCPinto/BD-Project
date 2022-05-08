
from flask import Blueprint, jsonify, request
from flask_jwt_extended import decode_token

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

    if "type" not in args or "description" not in args or "height" not in args or "weight" not in args or "colour" not in args or "stock" not in args or "price" not in args or "token" not in args:

        return jsonify({
            "status": GET_ERROR_CODE,
            "error": "Wrong parameters"
        })
    
    type        = args["type"]
    description = args["description"]
    height      = args["height"]
    weight      = args["weight"]
    colour      = args["colour"]
    stock       = args["stock"]
    price       = args["price"]
    token       = decode_token(args["token"])
    seller_id   = token["sub"]["id"]

    message = {}

    try:

        conn   = db.get_data_base()
        query = f"INSERT INTO product (type, description,height,weight,colour, stock, price,seller_customer_id_user ) VALUES ('{type}','{description}',{height},{weight},'{colour}',{stock},{price},{seller_id}); SELECT currval('product_id_prod_seq');"
        cursor = conn.cursor()
        cursor.execute(query)
        row   = cursor.fetchall()[0]

        cursor.close()
        conn.commit()
        
       
        cursor = conn.cursor()
        query2 = "UPDATE product SET product_id_prod = ((select max(product_id_prod) from product)+1) where product_id_prod is null;"
        cursor.execute(query2)
        
        cursor.close()
        conn.commit()
        
        
        conn.close()
        message["status"]  = SUCCESS_CODE
        message["message"] = "Product added successfully"
        message["results"] = row[0]

        '''
        
        with db.get_data_base() as conn:
            with conn.cursor() as cursor:                
                query = f"INSERT INTO product (type, description,height,weight,colour, stock, price,seller_customer_id_user ) VALUES ('{type}','{description}',{height},{weight},'{colour}',{stock},{price},{seller_customer_id_user}); SELECT currval('product_id_prod_seq');"
                print("aaa1")
                cursor.execute(query)
                print("aaa")
                query2 = "UPDATE product SET product_id_prod = ((select max(product_id_prod) from product)+1) where product_id_prod is null;"
                cursor.execute(query2)
                print("222")
                row   = cursor.fetchall()[0]
                message["status"]  = SUCCESS_CODE
                message["message"] = "Product added successfully"
                message["results"] = row[0]
        '''
            

    except:
        return jsonify({
            "status": POST_ERROR_CODE,
            "error": "Something wrong happened"
        })


    return jsonify(message)


#ERRO NA SEGUNDA QUERY PROBABLY
@product.route("/<int:prod_id>", methods = ["POST"])
def refresh_product(prod_id):

    try:
        args = request.get_json()
    except:
        return jsonify({
            "status": GET_ERROR_CODE,
            "error": "No json"
        })

    if  "description" not in args or "height" not in args or "weight" not in args or "colour" not in args or "price" not in args :

        return jsonify({
            "status": GET_ERROR_CODE,
            "error": "Wrong parameters"
        })
    
    description = args["description"]
    price = args["price"]
    height  = args["height"]
    weight = args["weight"]
    colour = args["colour"]


    query   = f"SELECT * FROM product WHERE id_prod = {prod_id}"
    message = {}

    #RETORNAR ID????
    try:
        with db.get_data_base() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)

                if cursor.rowcount ==0:
                    message["status"] = GET_ERROR_CODE
                    message["error"]  = "Product id invalid"

                else:
                    #ERRO AQUI PROBABLY
                    query = f"""INSERT INTO product (type, description,height,weight,colour, stock, price,product_id_prod,seller_customer_id_user )
                             VALUES ((select type from product where id_prod = {prod_id}),'{description}',{height},{weight},'{colour}',(select stock from product where id_prod = {prod_id}),{price},{prod_id},(select seller_customer_id_user from product where id_prod = {prod_id})); SELECT currval('product_id_prod_seq');"""

                    cursor.execute(query)
                    row   = cursor.fetchall()[0]                 
                    message["status"]  = SUCCESS_CODE
                    message["message"] = "Product values updated"
                    message["results"] = row[0]


    except:
        return jsonify({
            "status": POST_ERROR_CODE,
            "error": "Something wrong happened"
        })


    return jsonify(message)