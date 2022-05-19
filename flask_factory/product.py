
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
                    #print("AQUIII")
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




@product.route("/<int:prod_id>", methods = ["GET"])
def query_detailes(prod_id):

    message = {}



    query = f"""select product.version, product.description, product.stock, product.price, product.weight, 
                       product.height, product.colour, coalesce(avg(rating.rating), -1) rating, coalesce(forum.comment, 'No comments')
                  from product  
                  full join rating on product.id_prod = rating.product_id_prod 
                  full join forum  on product.id_prod = forum.product_id_prod 
                 where product.id_prod = {prod_id} 
                 group by product.id_prod, product.version, forum.comment 
                 order by product.version;"""


    try:
        with db.get_data_base() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

                if cursor.rowcount!= 0:
                    description = []
                    stock       = []
                    price       = []
                    weight      = []
                    height      = []
                    colour      = []
                    rating      = []
                    comments    = []

                    for row in rows:
                        description.append(row[1])
                        stock.append(row[2])
                        price.append(row[3])
                        weight.append(row[4])
                        height.append(row[5])
                        colour.append(row[6])
                        rating.append(row[7])
                        comments.append(row[8])

                    message["status"]      = SUCCESS_CODE
                    message["description"] = description
                    message["stock"]       = stock
                    message["price"]       = price
                    message["weight"]      = weight
                    message["height"]      = height
                    message["colour"]      = colour
                    message["rating"]      = rating
                    message["comments"]    = comments

                else:
                    message["status"] = GET_ERROR_CODE
                    message["error"]  = "No product with that id"

    except:
        return jsonify({
            "status": POST_ERROR_CODE,
            "error": "Something wrong happened"
        })


    return jsonify(message)
