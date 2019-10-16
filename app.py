# import flask dependencies
from flask import Flask, request, jsonify
import os
import pymysql.cursors
import json
from datetime import date
import telebot
from fpdf import FPDF

bot = telebot.TeleBot(token='816398857:AAEZGcAQZO0QR1kYqEBV7nZTFWzNv2gD26g')

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

    if intent_name == 'menu':
        return menu(data)

    elif intent_name == 'menu.pengajuan.dagang':
        return perdagangan()

    elif intent_name == 'surat_pengantar_dagang_detail - notlpnusaha':
        return dataUserPengaju(data)

    elif intent_name == 'pengajuan_reklame':
        return reklame()

    elif intent_name == 'pengajuan_reklame_form - tglacara':
        return formReklame(data)

    return jsonify(request.get_json())

def menu(data):
    cekUserID = data.get("originalDetectIntentRequest").get("payload").get("from").get("id")
    idPesan = data.get("originalDetectIntentRequest").get("payload").get("message_id")
    isiPesan = data.get("originalDetectIntentRequest").get("payload").get("text")
    userNama = data.get("originalDetectIntentRequest").get("payload").get("from").get("username")
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
                        "subtitle": "Halo {}, Silahkan pilih menu di bawah".format(userNama),
                        "buttons": [
                            {
                                "text": "Surat izin Usaha Perdagangan",
                                "postback": "usaha perdagangan"
                            },
                            {
                                "text": "Pengajuan Izin Reklame",
                                "postback": "pengajuan reklame"
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
                            "text": "Form Pendaftaran",
                            "postback": "form perdagangan"
                        },
                        {
                            "text": "Syarat Pengajuan Perdagangan",
                            "postback": "syarat Perdagangan"
                        }
                    ]
                }
            }
        ]
    }
    return response

def reklame():
    response = {
        'fulfillmentMessages': [
            {
                "card": {
                    "title": "Izin Reklame",
                    "subtitle": "Silahkan pilih layanan di Bawah",
                    "buttons": [
                        {
                            "text": "Form Pendaftaran",
                            "postback": "form reklame"
                        },
                        {
                            "text": "Syarat Pemasangan Reklame",
                            "postback": "syarat reklame"
                        }
                    ]
                }
            }
        ]
    }
    return response

def dataUserPengaju(data):
    parameter_index = 0
    outputContexts = data['queryResult']['outputContexts']

    for index, parameter in enumerate(outputContexts):
        if parameter['name'] == "projects/otonlogybot-jsiadw/agent/sessions/" \
                                "53cffdfa-98d0-3832-8930-b0dd520ef777/contexts/surat_pengantar_dagang-nama-followup":
            parameter_index = index

    cekUserID = data.get("originalDetectIntentRequest").get("payload").get("from").get("id")
    namauser = outputContexts[parameter_index]['parameters']['namauser']
    nikuser = outputContexts[parameter_index]['parameters']['nik']
    alamat = outputContexts[parameter_index]['parameters']['alamat']
    notlpn = outputContexts[parameter_index]['parameters']['notlpn']
    namausaha = outputContexts[parameter_index]['parameters']['namausaha']
    alamatusaha = outputContexts[parameter_index]['parameters']['alamatusaha']
    jenisusaha = outputContexts[parameter_index]['parameters']['jenisusaha']
    notlpnusaha = outputContexts[parameter_index]['parameters']['notlpnusaha']

    try:
        result = ""
        with connection.cursor() as cursor:
            sql = "INSERT INTO tb_user_pengaju (id_user, nik, nama_user, alamat, no_tlp, tanggal) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (cekUserID, nikuser, namauser, alamat, notlpn, date.today().strftime("%Y-%m-%d")))
            id_inbox = cursor.lastrowid
            sql2 = "INSERT INTO tb_detail_user_pengaju (id_user_pengaju, nama_usaha, alamat_usaha, jenis_usaha, no_tlpn_usaha) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql2, (id_inbox, namausaha, alamatusaha, jenisusaha, notlpnusaha,))
            result = cursor.fetchone()
        connection.commit()

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="TESTING", ln=1, align="J")
        pdf.output("test.pdf")

        bot.send_document(cekUserID, open('test.pdf','rb'))

        response = {
            'fulfillmentText': "Selamat, data anda berhasil di masukan"
        }
        return jsonify(response)

    except Exception as error:
        print(error)

        response = {
            'fulfillmentText': "Data anda gagal di Daftarkan"
        }
        return jsonify(response)

def formReklame(data):
    parameter_index = 0
    outputContexts = data['queryResult']['outputContexts']

    for index, parameter in enumerate(outputContexts):
        if parameter['name'] == "projects/otonlogybot-jsiadw/agent/sessions/" \
                                "53cffdfa-98d0-3832-8930-b0dd520ef777/contexts/pengajuan_reklame_form-followup":
            parameter_index = index

    cekUserID = data.get("originalDetectIntentRequest").get("payload").get("from").get("id")
    namauser = outputContexts[parameter_index]['parameters']['namapenga']
    namaacara = outputContexts[parameter_index]['parameters']['namaacara']
    tglacara = outputContexts[parameter_index]['parameters']['tglacara']


    try:
        result = ""
        with connection.cursor() as cursor:
            sql = "INSERT INTO tb_reklame (id_user, nama_pengaju, nama_acara, tanggal_acara, tanggal_pengajuan) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (cekUserID, namauser, namaacara, tglacara, date.today().strftime("%Y-%m-%d")))
            result = cursor.fetchone()
        connection.commit()

        response = {
            'fulfillmentText': "Selamat, data anda berhasil di masukan"
        }
        return jsonify(response)

    except Exception as error:
        print(error)
        response = {
            'fulfillmentText': "Data anda gagal di Daftarkan"
        }
    return jsonify(response)



# run the app
if __name__ == '__main__':
   app.run(port=PORT, host='0.0.0.0')