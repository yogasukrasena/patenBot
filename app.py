# import flask dependencies
from flask import Flask, request, jsonify
import os
import pymysql.cursors
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

    if intent_name == 'webhook-intent':
        return Webhook(data)

    return jsonify(data)

def Webhook(data):
    pesan = data.get("queryResult").get("queryText")

    response = {
        'fulfillmentText': pesan
    }

    return jsonify(response)

# run the app
if __name__ == '__main__':
   app.run(port=PORT, host='0.0.0.0')