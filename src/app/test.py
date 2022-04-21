from urllib import response

from requests import request
import api

BASE = "127.0.0.1:5000/"

response = request.get(BASE + "login")
print(response.json())