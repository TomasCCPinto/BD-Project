from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, decode_token

from status.status import *
import database.db as db


stats = Blueprint("stats", __name__, url_prefix="/api/report")

@stats.route("/year", methods=["GET"])
def estatisticas():
    
    message={}

    query = f"""SELECT
                    DATE_TRUNC('month',order_date),
                    COUNT(total) ,
	                sum(total)	   
                FROM to_order
                where (date_part('year', (to_order.order_date)) < date_part('year', (select current_date)) and date_part('month', (to_order.order_date)) > date_part('month', (select current_date))) 
                        or (date_part('year', (to_order.order_date)) = date_part('year', (select current_date)) and date_part('month', (to_order.order_date)) <= date_part('month', (select current_date)) )  
                GROUP BY DATE_TRUNC('month',order_date);"""

    try:
        with db.get_data_base() as conn:
            with conn.cursor() as cursor:
                
                cursor.execute(query)
                
                rows = cursor.fetchall()
                
                results=[]
                for row in rows:
                    line = str(row[0]).split('-')
                    
                    res={}
                    res["month"]=line[1]+'-'+line[0]
                    res["total_value"]=row[2]
                    res["orders"]=row[1]
                    results.append(res)
                    
                message["status"] = SUCCESS_CODE
                message["results"] = results
                
    except:
        return jsonify({
            "status": POST_ERROR_CODE,
            "error": "Something wrong happened"
        })


    return jsonify(message)
