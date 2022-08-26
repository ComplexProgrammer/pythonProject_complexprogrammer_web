import base64
import datetime
import io
import os
import sqlite3
import urllib

import imutils
import numpy
import numpy as np
from PIL import Image, ImageChops, ImageFile
# from cv2 import cv2
import cv2
import urllib3
from skimage.metrics import structural_similarity as compare_ssim
from flask import render_template, request, jsonify, flash
from werkzeug.utils import secure_filename
import googletrans
from googletrans import Translator
import pyttsx3

from website import app, ALLOWED_EXTENSIONS, db
import json

from website.models import Users, Chat, ChatMessage, ChatUserRelation


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


# region online services


@app.route("/exchangerates")
def exchangerates():
    return render_template('exchangerates.html')


@app.route("/GetExchangeRates", methods=['GET'])
def GetExchangeRates():
    print(1)
    # url = "http://195.158.6.195:4444/Api/C0mplexApi/GetExchangeRates"
    url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
    r = urllib.request.urlopen(url)
    data = r.read()
    return {"data": json.loads(data)}


@app.route("/changetext", methods=['GET', 'POST'])
def changetext():
    return render_template('changetext.html')


@app.route("/ChangeTextData", methods=['POST'])
def GetChangeTextData():
    text = request.args.get('text')
    characters = [["A", "А"], ["B", "Б"], ["D", "Д"], ["E", "Е"], ["F", "Ф"], ["G", "Г"], ["H", "Ҳ"], ["I", "И"],
                  ["J", "Ж"], ["K", "К"], ["L", "Л"], ["M", "М"], ["N", "Н"], ["O", "О"], ["P", "П"], ["Q", "Қ"],
                  ["R", "Р"], ["S", "С"], ["T", "Т"], ["U", "У"], ["V", "В"], ["X", "Х"], ["Y", "Й"], ["Z", "З"],
                  ["a", "а"], ["b", "б"], ["d", "д"], ["e", "е"], ["f", "ф"], ["g", "г"], ["h", "ҳ"], ["i", "и"],
                  ["j", "ж"], ["k", "к"], ["l", "л"], ["m", "м"], ["n", "н"], ["o", "о"], ["p", "п"], ["q", "қ"],
                  ["r", "р"], ["s", "с"], ["t", "т"], ["u", "у"], ["v", "в"], ["x", "х"], ["y", "й"], ["z", "з"],
                  ["А", "A"], ["Б", "B"], ["С", "C"], ["Ч", "Ch"], ["Д", "D"], ["Е", "E"], ["Ф", "F"], ["Г", "G"],
                  ["Ҳ", "H"], ["И", "I"], ["Ж", "J"], ["К", "K"], ["Л", "L"], ["М", "M"], ["Н", "N"], ["О", "O"],
                  ["П", "P"], ["Қ", "Q"], ["Р", "R"], ["С", "S"], ["Ш", "Sh"], ["Т", "T"], ["У", "U"], ["В", "V"],
                  ["Х", "X"], ["Й", "Y"], ["Я", "Ya"], ["Ю", "Yu"], ["Ё", "Yo"], ["З", "Z"], ["Ғ", "Gʼ"], ["а", "a"],
                  ["б", "b"], ["с", "c"], ["ч", "ch"], ["д", "d"], ["е", "e"], ["ф", "f"], ["г", "g"], ["ҳ", "h"],
                  ["и", "i"], ["ж", "j"], ["к", "k"], ["л", "l"], ["м", "m"], ["н", "n"], ["о", "o"], ["п", "p"],
                  ["қ", "q"], ["р", "r"], ["с", "s"], ["ш", "sh"], ["т", "t"], ["у", "u"], ["в", "v"], ["х", "x"],
                  ["й", "y"], ["я", "ya"], ["ю", "yu"], ["ё", "yo"], ["з", "z"], ["ғ", "gʼ"], ["ъ", "`"], ["`", "ъ"],
                  ["'", "ъ"]]

    lotin = False
    arr = list(text)
    for ar in arr:
        if 0 < ord(ar) < 1024:
            lotin = True
        for obj in characters:
            if obj[0] == ar:
                text = text.replace(ar, obj[1])

    if lotin:
        text = text.replace("Оъ", "Ў").replace("оъ", "ў")
        text = text.replace("йа", "я").replace("Йа", "Я").replace("ЙА", "Я").replace("йА", "я")
        text = text.replace("йо", "ё").replace("Йо", "Ё").replace("ЙО", "Ё").replace("йО", "ё")
        text = text.replace("йу", "ю").replace("Йу", "Ю").replace("ЙУ", "Ю").replace("йУ", "ю")
        text = text.replace("сҳ", "ш").replace("Сҳ", "Ш").replace("СҲ", "Ш").replace("сҲ", "ш")
        text = text.replace("cҳ", "ч").replace("Cҳ", "Ч").replace("CҲ", "Ч").replace("cҲ", "ч")
        text = text.replace("Гъ", "Ғ").replace("гъ", "ғ")
    else:
        text = text.replace("Я", "Ya").replace("я", "ya")
        text = text.replace("Ё", "Yo").replace("ё", "yo")
        text = text.replace("Ю", "Yu").replace("ю", "yu")
        text = text.replace("Ш", "Sh").replace("ш", "sh")
        text = text.replace("Ч", "Ch").replace("ч", "ch")
        text = text.replace("Ў", "Oʼ").replace("ў", "oʼ")
        text = text.replace("Ғ", "Gʼ").replace("ғ", "gʼ")

    return text


@app.route("/ip")
def ip():
    return render_template('ip.html')


@app.route("/GetMyIP", methods=['GET'])
def GetMyIP():
    url = "https://ipapi.co/ip"
    r = urllib.request.urlopen(url)
    data = r.read()
    print(data)
    return data


@app.route("/GetMyIPData", methods=['GET'])
def GetMyIPData():
    url = "https://ipapi.co/json"
    r = urllib.request.urlopen(url)
    data = r.read()
    return {"data": json.loads(data)}


@app.route("/GetCustomIPData", methods=['GET'])
def GetCustomIPData():
    ip = request.args.get('ip')
    url = "https://ipapi.co/" + ip + "/json"
    r = urllib.request.urlopen(url)
    data = r.read()
    return {"data": json.loads(data)}


@app.route("/avtotest/")
@app.route("/avtotest/<id>")
def avtotest(id='0'):
    return render_template('avtotest.html', bilet=id)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route("/GetSavol", methods=['GET'])
def GetSavol():
    bilet = request.args.get('bilet')
    conn = sqlite3.connect('website/avtotest.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    if (bilet):
        savol = cur.execute('SELECT * FROM savollar where bilet=="' + bilet + '" order by raqam;').fetchall()
    else:
        savol = cur.execute('SELECT * FROM savollar order by raqam;').fetchall()

    return jsonify(savol)


@app.route("/GetBilet", methods=['GET'])
def GetBilet():
    conn = sqlite3.connect('website/avtotest.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    savol = cur.execute('SELECT bilet FROM savollar group by bilet order by bilet;').fetchall()
    return jsonify(savol)


@app.route('/uploadfile')
def UploadImage():
    return render_template('uploadfile.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/imagecompare')
def ImageCompare():
    return render_template('imagecompare.html')


def ImageCompare(image1, image2, grayA, grayB):
    (score, diff0) = compare_ssim(grayA, grayB, full=True)
    diff0 = (diff0 * 255).astype("uint8")
    print("SSIM: {}".format(score))
    thresh = cv2.threshold(diff0, 0, 255,
                           cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for c in cnts:
        # compute the bounding box of the contour and then draw the
        # bounding box on both input images to represent where the two
        # images differ
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(image1, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(image2, (x, y), (x + w, y + h), (0, 0, 255), 2)
    im_arr = cv2.imencode('.jpg', thresh)[1].tostring()  # im_arr: image in Numpy one-dim array format.
    base64_str = "data:image/png;base64," + base64.b64encode(im_arr).decode('utf-8')
    # im_bytes = im_arr.tobytes()
    # im_b64 = base64.b64encode(im_bytes)
    return {"data": base64_str}


@app.route("/GetImageCompareResult", methods=['POST'])
def GetImageCompareResult():
    if 'img1' not in request.files or 'img2' not in request.files:
        print('No file part')
        return {"data": ''}
    else:
        img1_model = request.files['img1']
        img2_model = request.files['img2']
        print(img1_model)
        print(img2_model)
        image1 = np.asarray(bytearray(img1_model.read()), dtype="uint8")
        image1 = cv2.imdecode(image1, cv2.IMREAD_COLOR)
        image2 = np.asarray(bytearray(img2_model.read()), dtype="uint8")
        image2 = cv2.imdecode(image2, cv2.IMREAD_COLOR)
        # grayA = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        # grayB = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        grayA = cv2.cvtColor(image1, cv2.COLOR_BGRA2GRAY)
        grayB = cv2.cvtColor(image2, cv2.COLOR_BGRA2GRAY)
        height1, width1, channels1 = image1.shape
        height2, width2, channels2 = image2.shape
        print(height1, width1, channels1)
        print(height2, width2, channels2)
        if width1 == width2 and height1 == height2:
            return ImageCompare(image1, image2, grayA, grayB)
        else:
            dim = (512, 512)
            resized_image1 = cv2.resize(grayA, dim, interpolation=cv2.INTER_AREA)
            resized_image2 = cv2.resize(grayB, dim, interpolation=cv2.INTER_AREA)
            return ImageCompare(image1, image2, grayA, resized_image1)
            # ImageFile.LOAD_TRUNCATED_IMAGES = True
            # img1 = Image.open(img1_model)
            # img2 = Image.open(img2_model)
            #
            # diff = ImageChops.difference(img1, img2)
            # print(diff.getbbox())
            # with io.BytesIO() as output:
            #     diff.save(output, format="png")
            #     contents = output.getvalue()
            #     result = "data:image/png;base64," + base64.b64encode(contents).decode('utf-8')
            #     # print(result)
            #     return {"data": result}


@app.route('/translate')
def C0mplexTranslate():
    return render_template('translate.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route("/getUser", methods=['POST'])
def getUser():
    user_id = request.args.get('id')
    name = request.args.get('name')
    email = request.args.get('email')
    phone = request.args.get('phone')
    provider_id = request.args.get('provider_id')
    uid = request.args.get('uid')
    email_verified = request.args.get('email_verified')
    not_me = request.args.get('not_me')
    user = Users.query.all()
    if not_me:
        user = Users.query.filter(Users.uid != uid).all()
    else:
        if name:
            user = Users.query.filter(Users.name == name).all()
        if email:
            user = Users.query.filter(Users.email == email).all()
        if phone:
            user = Users.query.filter(Users.phone == phone).all()
        if uid:
            user = Users.query.filter(Users.uid == uid).all()

    return jsonify([s.toDict() for s in user])


@app.route('/checkUser', methods=['POST'])
def CheckUser():
    json = request.json
    print(json)
    photo_url = json['photo_url']
    name = json['name']
    email = json['email']
    phone = json['phone']
    provider_id = json['provider_id']
    uid = json['uid']
    email_verified = json['email_verified']
    # user = Users.query.filter_by(uid=uid).first()
    user = Users.query.filter_by(uid=uid).all()
    if user is None:
        user = Users(photo_url=photo_url, name=name, email=email, phone=phone, provider_id=provider_id, uid=uid,
                     email_verified=email_verified, created_date=datetime.datetime.now(),
                     login_date=datetime.datetime.now(), login_count=1, active=1)
        db.session.add(user)
        db.session.commit()
    else:
        user[0].login_date = datetime.datetime.now()
        user[0].login_count = user[0].login_count + 1
        user[0].active = 1
        db.session.commit()
    print(user)
    print(type(user))
    print(user[0].email)
    return jsonify([s.toDict() for s in user])


@app.route('/logout', methods=['POST'])
def logout():
    uid = request.args.get('uid')
    user = Users.query.filter_by(uid=uid).first()
    if user is not None:
        user.logout_date = datetime.datetime.now()
        user.logout_count = user.logout_count + 1
        user.active = 0
        db.session.commit()
    return uid


@app.route('/getChatMessageByUserId', methods=['POST'])
def getChatMessageByUserId():
    user_id = request.args.get('user_id')
    result = ChatMessage.query.join(Chat, Chat.id == ChatMessage.chat_id).join(ChatUserRelation, ChatUserRelation.chat_id == Chat.id).filter(ChatUserRelation.user_id == user_id).all()
    query = db.session.query(
        Chat.type,
        ChatMessage.text,
        ChatMessage.sender_id,
        ChatUserRelation.count_new_message,
        ChatUserRelation.user_id,
        ChatUserRelation.chat_id,
    )
    join_query = query.join(ChatMessage).join(ChatUserRelation).filter(ChatUserRelation.user_id == user_id)
    print(join_query.all())
    results = join_query.all()
    # results = db.session.query(ChatMessage.text, Chat.id, Chat.type).join(Chat).all()
    results = [tuple(row) for row in results]

    json_string = json.dumps(results)
    return {"data": json.loads(json_string)}
    # return jsonify([s.toDict() for s in result])


@app.route('/sendMessage', methods=['POST'])
def sendMessage():
    json_data = request.json
    print(json)
    chat_id = json_data['chat_id']
    sender_id = json_data['sender_id']
    receiver_id = json_data['receiver_id']
    text = json_data['text']
    chat = Chat.query.filter_by(id=chat_id).first()
    if chat is None:
        chat = Chat(type=0, created_by=sender_id, created_date=datetime.datetime.now())
        db.session.add(chat)
        chat_message = ChatMessage(chat_id=chat.id, type=1, text=text, sender_id=sender_id, created_by=sender_id,
                                   created_date=datetime.datetime.now())
        db.session.add(chat_message)
        chat_user_relation = ChatUserRelation(user_id=receiver_id, chat_id=chat.id, count_new_message=1)
        db.session.add(chat_user_relation)
        db.session.commit()
    else:
        # query = db.session.query(
        #     Chat.type,
        #     ChatMessage.text,
        #     ChatMessage.sender_id,
        #     ChatUserRelation.count_new_message,
        #     ChatUserRelation.message_view,
        #     ChatUserRelation.user_id,
        #     ChatUserRelation.chat_id,
        # )
        # chat_message = query.join(ChatMessage).join(ChatUserRelation).filter(Chat.id == chat_id).all()
        chat.last_modified_by = sender_id
        chat.last_modified_date = datetime.datetime.now()
        chat_message = ChatMessage(chat_id=chat_id, type=1, text=text, sender_id=sender_id, created_by=sender_id,
                                   created_date=datetime.datetime.now())
        db.session.add(chat_message)
        chat_user_relation = ChatUserRelation.query.filter_by(chat_id=chat_id).first()
        chat_user_relation.count_new_message = chat_user_relation.count_new_message+1
        db.session.commit()
    return {"data": ""}


@app.route('/GetTranslateLanguages', methods=['POST'])
def GetTranslateLanguages():
    return {'data': googletrans.LANGUAGES}


@app.route("/GetTranslateResult", methods=['POST'])
def GetTranslateResult():
    text = request.args.get('text')
    src = request.args.get('src')
    dest = request.args.get('dest')
    print(src)
    print(dest)
    # text = '''
    # A Római Birodalom (latinul Imperium Romanum) az ókori Róma által létrehozott
    # államalakulat volt a Földközi-tenger medencéjében
    # '''
    print(text)
    translator = Translator()

    # result = translator.translate(text)
    result = translator.translate(text, src=src, dest=dest)
    print(result.src)
    print(result.dest)
    print(result.origin)
    print(result.text)
    print(result.pronunciation)
    return {"data": result.text}


@app.route("/TextToSpeech", methods=['POST'])
def TextToSpeech():
    text = request.args.get('text')
    text_speech = pyttsx3.init()
    text_speech.say(text)
    text_speech.runAndWait()
    return {"data": text}


@app.route('/coins')
def coins():
    return render_template('coins.html')


@app.route("/GetCoins", methods=['GET'])
def GetCoins():
    url = "https://api.minerstat.com/v2/coins"
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    htmlSource = r.data
    # r = urllib3.request.urlopen(url)
    # data = r.read()
    return {"data": json.loads(htmlSource)}


@app.route('/chat')
def chat():
    return render_template('chat.html')


@app.route('/chat2')
def chat2():
    return render_template('chat2.html')


@app.route('/chat3')
def chat3():
    return render_template('chat3.html')


# endregion


# region online games
@app.route('/snake')
def snake():
    return render_template("snake.html")


@app.route('/snake2')
def snake2():
    return render_template("snake2.html")


@app.route('/car')
def car():
    return render_template("car.html")


@app.route('/duckhunt')
def duckhunt():
    return render_template("duckhunt.html")


@app.route('/motorcycle')
def motorcycle():
    return render_template("motorcycle.html")


@app.route('/bubbleshooter')
def bubbleshooter():
    return render_template("bubbleshooter.html")


@app.route('/pingpong')
def pingpong():
    return render_template("pingpong.html")


@app.route('/tictactoe')
def tictactoe():
    return render_template("tictactoe.html")


@app.route('/tetris')
def tetris():
    return render_template("tetris.html")

# endregion
