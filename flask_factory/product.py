
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
    query = f"Select * from seller where customer_id_user = {seller_id};"

    try:

        with db.get_data_base() as conn:
            with conn.cursor() as cursor: 
                cursor.execute(query)
                
                if cursor.rowcount == 1:
                    query = f"INSERT INTO product (id_prod,version ,type, description,height,weight,colour, stock, price,seller_customer_id_user ) VALUES ((select max(id_prod)+1 from product),0,'{type}','{description}',{height},{weight},'{colour}',{stock},{price},{seller_id});"
                    cursor.execute(query)
                    
                    query_return = "select max(id_prod) from product;"
                    
                    cursor.execute(query_return)
                    print("AQUIII")
                    row   = cursor.fetchall()[0]


                    message["status"]  = SUCCESS_CODE
                    message["message"] = "Product added successfully"
                    message["results"] = row[0]


                else:
                    message["status"] = GET_ERROR_CODE
                    message["error"]  = "Only sellers can manage products"
        

    except:
        return jsonify({
            "status": POST_ERROR_CODE,
            "error": "Something wrong happened"
        })


    return jsonify(message)



@product.route("/<int:prod_id>", methods = ["PUT"])
def update_product(prod_id):

    try:
        args = request.get_json()
    except:
        return jsonify({
            "status": GET_ERROR_CODE,
            "error": "No json"
        })

    if  "description" not in args or "height" not in args or "weight" not in args or "colour" not in args or "price" not in args or "token" not in args :

        return jsonify({
            "status": GET_ERROR_CODE,
            "error": "Wrong parameters"
        })
    
    description = args["description"]
    price = args["price"]
    height  = args["height"]
    weight = args["weight"]
    colour = args["colour"]
    token       = decode_token(args["token"])
    seller_id   = token["sub"]["id"]

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
                    query = f"select  version ,type ,stock, seller_customer_id_user from product where id_prod =  {prod_id} ;"
                    cursor.execute(query)
                    row   = cursor.fetchall()[-1] 

                    if(row[3]==seller_id):

                        version = row[0]+1
                        #print(row)
                        #print(str(version)+ ' '+ description + ' '+ str(price)+' '+str(height)+' '+str(weight)+ ' '+colour)
                        query = f"INSERT INTO product (id_prod,version,type, description,height,weight,colour, stock, price,seller_customer_id_user ) VALUES ({prod_id},{version},'{row[1]}','{description}',{height},{weight},'{colour}',{row[2]},{price},{row[3]});"
                        cursor.execute(query)
                                        
                        message["status"]  = SUCCESS_CODE
                        message["message"] = "Product values updated"
                        #message["results"] = row[0]
                        
                    else:
                        message["status"] = GET_ERROR_CODE
                        message["error"]  = "Only the product seller can update it"


    except:
        return jsonify({
            "status": POST_ERROR_CODE,
            "error": "Something wrong happened"
        })


    return jsonify(message)