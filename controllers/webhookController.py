import sys
from flask import jsonify, request
from models import db, LineUser, Keyword, Product, Pelanggan
from dotenv import load_dotenv
from line import Configuration, MessageHandler, ReplyMessage, ReplyFlexMessage, GetProfile
from phonenumbers import is_valid_number as valid_number, parse as pp
from utils import helper
import json
import os

load_dotenv()

secret = os.environ.get("FLASK_LINE_SECRET")
access_token = os.environ.get("FLASK_LINE_ACCESS_TOKEN")
line = Configuration(secret=secret, access_token=access_token)


handler = MessageHandler()

def index():
    if request.method == "POST":
        signature = request.headers.get('X-Line-Signature')
        message = request.get_data(as_text=True)
        try:
            handler.handler(signature=signature, body=message)
        except:
            return jsonify({"status": False, "message": "failed to verify signature"})
    return jsonify({"status": True, "message": "Webhook alive"})

@handler.onMessage
def onMessage(event):
    reply_token = event['replyToken']
    text_message: str = event['message']['text']
    user_id = event['source']['userId']
    user: LineUser = LineUser.query.filter_by(user_id=user_id).first()
    if user is None:
        profile = GetProfile(user_id=user_id)
        new_user = LineUser(user_id=user_id, display_name=profile.displayName, language=profile.language)
        db.session.add(new_user)
        db.session.commit()
    if user.last_action is not None:
        print(user.last_action)
        try:
            last_action = json.loads(user.last_action)
        except Exception as e:
            print(e)
        if last_action['action'] == "isi_data_nama":
            if len(text_message) < 1:
                ReplyMessage(reply_token=reply_token, text="anda tidak boleh mengkosongi nama anda")
                return
            last_action.update({"action": "isi_data_no_hp", "data":{"name": text_message}})
            ReplyMessage(reply_token=reply_token, text="Silahkan masukkan 'No Hp' anda\ncontoh : +628xxxxxxxxxxx")
        if last_action['action'] == "isi_data_no_hp":
            if len(text_message) < 1:
                ReplyMessage(reply_token=reply_token, text="anda tidak boleh mengkosongi no hp anda")
                return
            if not valid_number(pp(text_message)):
                ReplyMessage(reply_token=reply_token, text="Nomer Handphone anda tidak valid\nsilahkan ulangi masukkan no hp anda\ncontoh : +628xxxxxxxxxxx")
                return
            last_action.update({"action": "isi_data_alamat", "data":{"no_hp": text_message}})
            ReplyMessage(reply_token=reply_token, text="Silahkan masukkan 'No Hp' anda")
        print(last_action)
        user.last_action = str(last_action)
        db.session.commit()
        return
    list_keyword = Keyword.query.all()
    for keywords in list_keyword:
        if keywords.keywords in text_message.lower():
            ReplyMessage(reply_token=reply_token, text=keywords.answer)
            return
    ReplyMessage(reply_token=reply_token, text="Maaf, saya tidak bisa memahami pesanan anda")


@handler.onPostBack
def onPostBack(event):
    reply_token = event['replyToken']
    postBackData: str = event['postback']['data']
    user_id = event['source']['userId']
    user = LineUser.query.filter_by(user_id=user_id).first()
    if user is None:
        profile = GetProfile(user_id=user_id)
        new_user = LineUser(user_id=user_id, display_name=profile.displayName, language=profile.language)
        db.session.add(new_user)
        db.session.commit()
    if postBackData == "menu_list_product":
        products = Product.query.all()
        if len(products) < 1:
            ReplyMessage(reply_token=reply_token, text="Kami belum menambahkan product untuk saat init")
            return
        ReplyFlexMessage(user_id=user_id, text="List Product", data=helper.create_carousel_product(products=products))
        return
    elif postBackData == "menu_rekomendasi":
        ReplyMessage(reply_token=reply_token, text="List rekomendasi product")
        return
    elif postBackData == "menu_cara_memesan":
        ReplyMessage(reply_token=reply_token, text="Cara Memesan\n\n1. Silahkan pilih menu product atau rekemondasi product\n2. Kemudian pilih product yang anda inginkan\n3. Kemudian isi data yang di perlukan\n4. Kemudian anda dapat melanjutkan pembayaran dan menunggu konfirmasi oleh admin\n5. Enjoy...!")
        return
    elif postBackData == "menu_riwayat":
        ReplyMessage(reply_token=reply_token, text="Riwayat")
        return
    elif postBackData == "menu_tentang":
        ReplyMessage(reply_token=reply_token, text="Tentang")
        return
    elif "pesan_product_" in str(postBackData).lower():
        pelanggan = Pelanggan.query.filter_by(line_user_id=user.id).first()
        if pelanggan is None:
            last_action = {
                "action": "isi_data_nama",
                "data": {
                    "name": "",
                    "no_hp": "",
                    "alamat": "",
                    "kota_kab": "",
                    "provinsi": "",
                    "kode_pos": "",
                    "rt": "",
                    "rw": "",
                },
                "next_action": postBackData
            }
            user.last_action = json.dumps(last_action)
            db.session.commit()
            ReplyMessage(reply_token=reply_token, text="Data anda belum ada di database kami\nuntuk melanjutkan pesanan ini silahkan lengkapi dulu data diri anda\n\nSilahkan kirimkan Nama Lengkap anda di bawah ini")
            return

    
        