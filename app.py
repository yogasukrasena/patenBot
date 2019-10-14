# import flask dependencies
from flask import Flask, request, jsonify
import os
import pymysql.cursor
import json
from datetime import date

# initialize the flask app
app = Flask(__name__)
PORT = int(os.environ.get("PORT", 5000))

# create a route for webhook
@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    intent_name = data.get("queryResult").get("intent").get("displayName")
    print(data)

    return jsonify(data)

# run the app
if __name__ == '__main__':
   app.run(port=PORT, host='0.0.0.0')