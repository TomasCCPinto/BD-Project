
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, jsonify, request
#status e database
from status.status import *
import database.db as db


product = Blueprint("product", __name__, url_prefix="/api/product/")


@product.route("/add", methods = ["POST"])
def add_product():
    pass

