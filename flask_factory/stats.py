from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, decode_token

from status.status import *
import database.db as db


stats = Blueprint("stats", __name__, url_prefix="/api/")

@stats.route("/report/<int:year>", methods=["GET"])
def estatisticas(year):
    
    message={}

    query = f"""select month, sum(total) , count(*)  from to_order where year = {year} group by month """

    try:
        with db.get_data_base() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                
                results=[]
                for row in rows:
                    res={}
                    res["month"]=row[0]
                    res["total_value"]=row[1]
                    res["orders"]=row[2]
                    results.append(res)

                message["status"] = SUCCESS_CODE
                message["results"] = results
                
    except:
        return jsonify({
            "status": POST_ERROR_CODE,
            "error": "Something wrong happened"
        })


    return jsonify(message)
