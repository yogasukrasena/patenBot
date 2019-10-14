# import flask dependencies
from flask import Flask, request, jsonify
import os
import pymysql.cursors
import json
from datetime import date

# initialize the flask app
app = Flask(__name__)
PORT = int(os.environ.get("PORT", 5000))

connection = pymysql.connect(host='db4free.net',
                             user='yogasukrasena',
                             password='Ikadek07',
                             db='db_paten_yoga',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

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
    cekUserID = data.get("originalDetectIntentRequest").get("payload").get("data").get("from").get("id")
    id_pesan = data.get("originalDetectIntentRequest").get("payload").get("message_id")
    pesan = data.get("originalDetectIntentRequest").get("payload").get("text")
    id_inbox = ""

    try:
        result = None
        with connection.cursor() as cursor:
            sql = "SELECT * FROM tb_ WHERE tb_profile.userID = %s"
            cursor.execute(sql, (cekUserID))
            result = cursor.fetchone()

        response = {
            'fulfillmentMessages': [
                {
                    "card": {
                        "title": "Menu",
                        "subtitle": "Halo {}, Silahkan pilih menu di bawah".format(result['nama']),
                        "buttons": [
                            {
                                "text": "Cek Profil",
                                "postback": "cek profil"
                            },
                            {
                                "text": "Info Akademik",
                                "postback": "info akademik"
                            }
                        ]
                    }
                }
            ]
        }
        return jsonify(response)

    except Exception:
        response = {
            'fulfillmentText': "Akun anda belum terkait dengan Sistem Simak, mohon input nim Anda"
        }
        return jsonify(response)


# run the app
if __name__ == '__main__':
   app.run(port=PORT, host='0.0.0.0')