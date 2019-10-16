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
            id_inbox = cursor.lastrowid
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
        with connection.cursor() as cursor:
            sql = "INSERT INTO tb_outbox (id_inbox, response) VALUES (%s, %s)"
            cursor.execute(sql, (id_inbox, response))
            sql2 = "UPDATE tb_inbox SET tb_inbox.status = '1' WHERE tb_inbox.id_inbox = %s"
            cursor.execute(sql2, (id_inbox))
            result = cursor.fetchone()
        connection.commit()

        return response


    except Exception as error:
        print(error)
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
        pdf.cell(200, 10, txt="Pengajuan Surat Izin Usaha Perdagangan", ln=1, align="C")
        pdf.cell(200, 10, txt="Kecamatan Ubud, Kabupaten Gianyar, Provinsi Bali", ln=1, align="C")
        pdf.cell(200, 10, txt="Nama Pengaju : {}".format(namauser), ln=1, align="J")
        pdf.cell(200, 10, txt="Nik : {}".format(nikuser), ln=1, align="J")
        pdf.cell(200, 10, txt="Alamat : {}".format(alamat), ln=1, align="J")
        pdf.cell(200, 10, txt="Nomer Telepon : {}".format(notlpn), ln=1, align="J")
        pdf.cell(200, 10, txt="Usaha Pengaju", ln=1, align="C")
        pdf.cell(200, 10, txt="Nama Usaha : {}".format(namausaha), ln=1, align="J")
        pdf.cell(200, 10, txt="Alamat Usaha : {}".format(alamatusaha), ln=1, align="J")
        pdf.cell(200, 10, txt="Jenis Usaha : {}".format(jenisusaha), ln=1, align="J")
        pdf.cell(200, 10, txt="Nomer Telepon Usaha : {}".format(notlpnusaha), ln=1, align="J")
        pdf.output("form_pendaftaran.pdf")

        bot.send_document(cekUserID, open('form_pendaftaran.pdf','rb'))

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

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Pengajuan Surat Izin Pemasangan Baliho", ln=1, align="C")
        pdf.cell(200, 10, txt="Kecamatan Ubud, Kabupaten Gianyar, Provinsi Bali", ln=1, align="C")
        pdf.cell(200, 10, txt="Nomor: 156/C/PANPEL-{}/I/2019 ".format(namaacara), ln=1, align="J")
        pdf.cell(200, 10, txt="Lampiran: - ", ln=1, align="J")
        pdf.cell(200, 10, txt="Perihal: Permohonan Izin Pemasangan Baliho", ln=1, align="J")
        pdf.cell(200, 10, txt="Kepada : ", ln=1, align="J")
        pdf.cell(200, 10, txt="Yth. 	Camat ", ln=1, align="J")
        pdf.cell(200, 10, txt="Kecamatan Ubud", ln=1, align="J")
        pdf.cell(200, 10, txt="di-	", ln=1, align="J")
        pdf.cell(200, 10, txt="Tempat", ln=1, align="J")
        pdf.cell(200, 10, txt="Dengan hormat, ", ln=1, align="J")
        pdf.cell(200, 10, txt="Sehubungan dengan akan diselenggarakannya kegiatan {} oleh {} , ".format(namaacara, namauser), ln=1, align="J")
        pdf.cell(200, 10, txt="maka kami selaku panitia pelaksana mohon izin pemasangan baliho, pada:", ln=1, align="J")
        pdf.cell(200, 10, txt="Tanggal	: {} ".format(tglacara), ln=1, align="J")
        pdf.cell(200, 10, txt="Nama Acara	: {}".format(namaacara), ln=1, align="J")
        pdf.cell(200, 10, txt="Demikian surat permohonan ini kami sampaikan, besar harapan kami agar Bapak/Ibu bersedia ", ln=1, align="J")
        pdf.cell(200, 10, txt="dan berkenan untuk membantu mensukseskan acara tersebut. Atas perhatian dan bantuan ", ln=1, align="J")
        pdf.cell(200, 10, txt="Bapak/Ibu kami ucapkan terima kasih. ", ln=1, align="J")

        pdf.output("form_pendaftaran.pdf")

        bot.send_document(cekUserID, open('form_pendaftaran.pdf', 'rb'))

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