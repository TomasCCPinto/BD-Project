from flask import Flask, jsonify
from status import *

def creat_app(test_config = None):

    app = Flask(__name__)

    @app.route("/", methods = ["get"])
    def route():
        # read README file and return it
        return jsonify({"code": SUCCESS_CODE, "message" : "Welcome to our data base"})

    return app

