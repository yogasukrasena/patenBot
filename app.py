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
    cekUserID = data.get("originalDetectIntentRequest").get("payload").get("from").get("id")
    idPesan = data.get("originalDetectIntentRequest").get("payload").get("message_id")
    pesan = data.get("originalDetectIntentRequest").get("payload").get("text")
    print(data)

    try:
        result = ""
        with connection.cursor() as cursor:
            sql = "INSERT INTO tb_inbox (id_pesan, pesan, userID, tanggal) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (idPesan, pesan, cekUserID, date.today().strftime("%Y-%m-%d")))
            # idterakhir = cursor.lastrowid
            # sql = "INSERT INTO tb_outbox (id_inbox, pesan, date) VALUES (%s, %s, %s)"
            # cursor.execute(sql, (idterakhir, order(data), date.today().strftime("%Y-%m-%d")))
        connection.commit()
    except Exception:
        response = {
            'fulfillmentText': "Akun anda belum terkait dengan Sistem Simak, mohon input nim Anda"
        }
        return jsonify(response)
    finally:
        connection.close()

    if intent_name == 'webhook-intent':
        return Webhook(data)

def Webhook(data):

        response = {
            'fulfillmentMessages': [
                {
                    "card": {
                        "title": "Menu",
                        "subtitle": "Halo {}, Silahkan pilih menu di bawah",
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
        return response

    # except Exception:
    #     response = {
    #         'fulfillmentText': "Akun anda belum terkait dengan Sistem Simak, mohon input nim Anda"
    #     }
    #     return jsonify(response)


# run the app
if __name__ == '__main__':
   app.run(port=PORT, host='0.0.0.0')