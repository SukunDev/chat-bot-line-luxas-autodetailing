import sys
from flask import jsonify, request
from models import db, LineUser, Keyword, Product, Pelanggan, Transaksi, StatusPembayaran, StatusTransaksi, RekomendasiProduct
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
        except Exception as e:
            print(e)
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
        try:
            if user.last_action is not None:
                last_action = json.loads(user.last_action)
                action_data = last_action['data']
            else:
                last_action = {'action': None}
        except Exception as e:
            print(e)
        if last_action['action'] == "isi_data_nama":
            action_data.update({"name": text_message})
            last_action.update({"action": "isi_data_no_hp", "data":action_data})
            user.last_action = json.dumps(last_action)
            db.session.commit()
            ReplyMessage(reply_token=reply_token, text="Silahkan masukkan 'No Hp' anda\ncontoh : +628xxxxxxxxxxx")
            return
        if last_action['action'] == "isi_data_no_hp":
            try:
                if not valid_number(pp(text_message)):
                    ReplyMessage(reply_token=reply_token, text="Nomer Handphone anda tidak valid\nsilahkan ulangi masukkan no hp anda\ncontoh : +628xxxxxxxxxxx")
                    return
            except Exception as e:
                ReplyMessage(reply_token=reply_token, text="Nomer Handphone anda tidak valid\nsilahkan ulangi masukkan no hp anda\ncontoh : +628xxxxxxxxxxx")
                return
            action_data.update({"no_hp": text_message})
            last_action.update({"action": "isi_data_alamat_lengkap", "data":action_data})
            user.last_action = json.dumps(last_action)
            db.session.commit()
            ReplyMessage(reply_token=reply_token, text="Silahkan masukkan 'Alamat Lengkap' anda")
            return
        if last_action['action'] == "isi_data_alamat_lengkap":
            action_data.update({"alamat": text_message})
            last_action.update({"action": "isi_data_rt", "data":action_data})
            user.last_action = json.dumps(last_action)
            db.session.commit()
            ReplyMessage(reply_token=reply_token, text="Silahkan masukkan 'RT' anda")
            return
        if last_action['action'] == "isi_data_rt":
            action_data.update({"rt": text_message})
            last_action.update({"action": "isi_data_rw", "data":action_data})
            user.last_action = json.dumps(last_action)
            db.session.commit()
            ReplyMessage(reply_token=reply_token, text="Silahkan masukkan 'RW' anda")
            return
        if last_action['action'] == "isi_data_rw":   
            action_data.update({"rw": text_message})
            last_action.update({"action": "isi_data_kota", "data":action_data})
            user.last_action = json.dumps(last_action)
            db.session.commit()
            ReplyMessage(reply_token=reply_token, text="Silahkan masukkan 'kota / kab' anda")
            return
        if last_action['action'] == "isi_data_kota":
            action_data.update({"kota_kab": text_message})
            last_action.update({"action": "isi_data_provinsi", "data":action_data})
            user.last_action = json.dumps(last_action)
            db.session.commit()
            ReplyMessage(reply_token=reply_token, text="Silahkan masukkan 'Provinsi' anda")
            return
        if last_action['action'] == "isi_data_provinsi":
            action_data.update({"provinsi": text_message})
            last_action.update({"action": "isi_data_kode_pos", "data":action_data})
            user.last_action = json.dumps(last_action)
            db.session.commit()
            ReplyMessage(reply_token=reply_token, text="Silahkan masukkan 'kode pos' anda")
            return
        if last_action['action'] == "isi_data_kode_pos":
            action_data.update({"kode_pos": text_message})
            last_action.update({"action": "isi_data_confirm", "data":action_data})
            user.last_action = json.dumps(last_action)
            db.session.commit()
            ReplyMessage(reply_token=reply_token, text=f"Apakah data diri anda ini sudah benar\n\nNama : {action_data['name']}\nNo Hp : {action_data['no_hp']}\nAlamat : {action_data['alamat']}\nRT : {action_data['rt']}\nRW : {action_data['rw']}\nKota / Kab : {action_data['kota_kab']}\nProvinsi : {action_data['provinsi']}\nKode Pos : {action_data['kode_pos']}\n\nKetik YA / TIDAK untuk mengkonfirmasi data diri anda")
            return
        if last_action['action'] == "isi_data_confirm":
            if text_message.lower() == "ya":
                new_pelanggan = Pelanggan(
                    line_user_id=user.id,
                    name=action_data['name'],
                    no_hp=action_data['no_hp'],
                    alamat=action_data['alamat'],
                    kota_kab=action_data['kota_kab'],
                    provinsi=action_data['provinsi'],
                    kode_pos=action_data['kode_pos'],
                    rt=action_data['rt'],
                    rw=action_data['rw'],
                )
                db.session.add(new_pelanggan)
                user.last_action = json.dumps({"action": "next_confirm_product"})
                db.session.commit()
                product = Product.query.filter_by(id=int(last_action['next_action'].replace("pesan_product_", ""))).first()
                ReplyFlexMessage(user_id=user_id, text="Apakah anda ingin melanjutkan pesanan ini", data=helper.create_product_confirm(product=product))
                return
            if text_message.lower() == "tidak":
                last_action.update({"action": "isi_data_nama", "data":{"name": "","no_hp": "","alamat": "","kota_kab": "","provinsi": "","kode_pos": "","rt": "","rw": ""}})
                user.last_action = json.dumps(last_action)
                db.session.commit()
                ReplyMessage(reply_token=reply_token, text="Silahkan kirimkan Nama Lengkap anda di bawah ini")
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
    user: LineUser = LineUser.query.filter_by(user_id=user_id).first()
    if user is None:
        profile = GetProfile(user_id=user_id)
        new_user = LineUser(user_id=user_id, display_name=profile.displayName, language=profile.language)
        db.session.add(new_user)
        db.session.commit()
    try:
        if user.last_action is not None:
            last_action = json.loads(user.last_action)
        else:
            last_action = {'action': None}
    except Exception as e:
        print(e)
    if postBackData == "menu_list_product":
        products = Product.query.all()
        if len(products) < 1:
            ReplyMessage(reply_token=reply_token, text="Kami belum menambahkan product untuk saat init")
            return
        ReplyFlexMessage(user_id=user_id, text="List Product", data=helper.create_carousel_product(products=products))
        return
    elif postBackData == "menu_rekomendasi":
        rekomedasi = RekomendasiProduct.query.all()
        if len(rekomedasi) < 1:
            ReplyMessage(reply_token=reply_token, text="Kami belum menambahkan product untuk saat ini")
            return
        list_product = []
        for rekomen in rekomedasi:
            list_product.append(rekomen.product)
        ReplyFlexMessage(user_id=user_id, text="Rekomendasi Product", data=helper.create_carousel_product(products=list_product))
        return
    elif postBackData == "menu_riwayat":
        if len(user.transaksi) < 1:
            ReplyMessage(reply_token=reply_token, text="Anda tidak memiliki riwayat transaksi")
            return
        output_message = "List Riwayat"
        try:
            for transaksi in user.transaksi:
                product: Product = transaksi.product
                output_message += f"\n\nTransaksi #{transaksi.id}\n"
                output_message += f"Nama : {product.name}\n"
                output_message += f"Description : {product.description}\n"
                output_message += f"Price : Rp. {helper.format_uang(product.price)}\n"
                output_message += f"Status Transaksi : {transaksi.status_transaksi.value}\n"
                output_message += f"Status Pembayaran : {transaksi.status_pembayaran.value}\n"
                output_message += f"========================\n"
        except Exception as e:
            print(e)
        ReplyMessage(reply_token=reply_token, text=output_message)
        return
    elif "pesan_product_" in str(postBackData).lower():
        pelanggan = user.pelanggan
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
        else:
            user.last_action = json.dumps({"action": "next_confirm_product"})
            db.session.commit()
            product = Product.query.filter_by(id=int(postBackData.replace("pesan_product_", ""))).first()
            ReplyFlexMessage(user_id=user_id, text="Apakah anda ingin melanjutkan pesanan ini", data=helper.create_product_confirm(product=product))
            return
    elif "yes_next_confirm_product_" in str(postBackData).lower():
        if last_action['action'] != 'next_confirm_product':
            ReplyMessage(reply_token=reply_token, text="Maaf, saya tidak bisa memahami pesanan anda")
            return
        new_transaction = Transaksi(
            line_user_id=user.id,
            product_id=str(postBackData).replace("yes_next_confirm_product_",""),
            status_transaksi=StatusTransaksi.PENDING,
            status_pembayaran=StatusPembayaran.PENDING,
        )
        db.session.add(new_transaction)
        user.last_action = None
        db.session.commit()
        ReplyMessage(reply_token=reply_token, text="Pesanan anda telah kami terima. Silahkan selesaikan pembayaran untuk memproses pesanan")
        return
    elif "no_next_confirm_product_" in str(postBackData).lower():
        if last_action['action'] != 'next_confirm_product':
            ReplyMessage(reply_token=reply_token, text="Maaf, saya tidak bisa memahami pesanan anda")
            return
        user.last_action = None
        db.session.commit()
        ReplyMessage(reply_token=reply_token, text="Anda telah membatalkan pesanan")
        return
    
        