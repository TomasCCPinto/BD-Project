from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, decode_token

from status.status import *
import database.db as db
from User import User


forum = Blueprint("forum", __name__, url_prefix="/api/questions")


@forum.route("/<int:prod_id>", methods=["post"])
def make_comment(prod_id):
    
    try:
        args = request.get_json()
    except:
        return jsonify({
            "status": GET_ERROR_CODE,
            "error": "No json"
        })

    if "question" not in args or "token" not in args:
        return jsonify({
            "code": GET_ERROR_CODE,
            "message": "Wrong parameters"
        })

    question = args["question"]
    token       = decode_token(args["token"])
    questioner_id   = token["sub"]["id"]

    message = {}

    try:

        with db.get_data_base() as conn:
            with conn.cursor() as cursor: 
                query = f"INSERT INTO forum (comment,customer_id_user, forum_id_forum, product_id_prod, product_version) VALUES ('{question}',{questioner_id},null,{prod_id},(select max(version) from product where id_prod={prod_id})); select currval('forum_id_forum_seq');"
                cursor.execute(query)
                
                id_question = cursor.fetchall()[0]

                message["status"]  = SUCCESS_CODE
                message["message"] = "ORDER COMPLETED"
                message["result"] = id_question[0]

    except:
        return jsonify({
            "status": POST_ERROR_CODE,
            "error": "Something wrong happened"
        })


    return jsonify(message)    

    

    

    