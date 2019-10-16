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
        return Awal(data)

    elif intent_name == 'menu':
        return menu(data)

    elif intent_name == 'menu.pengajuan.dagang':
        return perdagangan()

    elif intent_name == 'surat_pengantar_dagang_detail - notlpnusaha':
        return dataUserPengaju()


    return jsonify(request.get_json())

def Awal(data):
    cekUserID = data.get("originalDetectIntentRequest").get("payload").get("from").get("id")
    idPesan = data.get("originalDetectIntentRequest").get("payload").get("message_id")
    isiPesan = data.get("originalDetectIntentRequest").get("payload").get("text")
    id_inbox = ""

    try:
        result = ""
        with connection.cursor() as cursor:
            sql = "INSERT INTO tb_inbox (id_pesan, pesan, userID, tanggal) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (idPesan, isiPesan, cekUserID, date.today().strftime("%Y-%m-%d")))
            # id_inbox = cursor.lastrowid
        connection.commit()

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

    except Exception:
        response = {
            'fulfillmentText': "Data anda gagal di Daftarkan"
        }
        return jsonify(response)

def menu(data):
    cekUserID = data.get("originalDetectIntentRequest").get("payload").get("from").get("id")
    idPesan = data.get("originalDetectIntentRequest").get("payload").get("message_id")
    isiPesan = data.get("originalDetectIntentRequest").get("payload").get("text")
    id_inbox = ""

    try:
        result = ""
        with connection.cursor() as cursor:
            sql = "INSERT INTO tb_inbox (id_pesan, pesan, userID, tanggal) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (idPesan, isiPesan, cekUserID, date.today().strftime("%Y-%m-%d")))
            # id_inbox = cursor.lastrowid
            result = cursor.fetchone()
        connection.commit()

        response = {
            'fulfillmentMessages': [
                {
                    "card": {
                        "title": "Menu",
                        "subtitle": "Halo {}, Silahkan pilih menu di bawah".format(isiPesan),
                        "buttons": [
                            {
                                "text": "Surat izin Usaha Perdagangan",
                                "postback": "usaha perdagangan"
                            },
                            {
                                "text": "Pengajuan Izin Reklame",
                                "postback": "izin reklame"
                            }
                        ]
                    }
                }
            ]
        }
        return response

    except Exception:
        response = {
            'fulfillmentText': "Data anda gagal di Daftarkan"
        }
        return jsonify(response)

def perdagangan():
    response = {
        'fulfillmentMessages': [
            {
                "card": {
                    "title": "SIUP",
                    "subtitle": "Silahkan pilih layanan di Bawah",
                    "buttons": [
                        {
                            "text": "Form Perdagangan",
                            "postback": "form perdagangan"
                        },
                        {
                            "text": "Syarat Pengajuan Perdagangan",
                            "postback": "Syarat"
                        }
                    ]
                }
            }
        ]
    }
    return response

def dataUserPengaju():

    response = {
        'fulfillmentText': "Data anda gagal di Daftarkan"
    }
    return jsonify(response)



# run the app
if __name__ == '__main__':
   app.run(port=PORT, host='0.0.0.0')