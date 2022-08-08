import base64
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
from skimage.metrics import structural_similarity as compare_ssim
from flask import render_template, request, jsonify, flash
from werkzeug.utils import secure_filename
import googletrans
from googletrans import Translator
import pyttsx3

from website import app, ALLOWED_EXTENSIONS
import json


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
    characrers = []
    characrers.append(["A", "А"])
    characrers.append(["B", "Б"])
    characrers.append(["D", "Д"])
    characrers.append(["E", "Е"])
    characrers.append(["F", "Ф"])
    characrers.append(["G", "Г"])
    characrers.append(["H", "Ҳ"])
    characrers.append(["I", "И"])
    characrers.append(["J", "Ж"])
    characrers.append(["K", "К"])
    characrers.append(["L", "Л"])
    characrers.append(["M", "М"])
    characrers.append(["N", "Н"])
    characrers.append(["O", "О"])
    characrers.append(["P", "П"])
    characrers.append(["Q", "Қ"])
    characrers.append(["R", "Р"])
    characrers.append(["S", "С"])
    characrers.append(["T", "Т"])
    characrers.append(["U", "У"])
    characrers.append(["V", "В"])
    characrers.append(["X", "Х"])
    characrers.append(["Y", "Й"])
    characrers.append(["Z", "З"])
    characrers.append(["a", "а"])
    characrers.append(["b", "б"])
    characrers.append(["d", "д"])
    characrers.append(["e", "е"])
    characrers.append(["f", "ф"])
    characrers.append(["g", "г"])
    characrers.append(["h", "ҳ"])
    characrers.append(["i", "и"])
    characrers.append(["j", "ж"])
    characrers.append(["k", "к"])
    characrers.append(["l", "л"])
    characrers.append(["m", "м"])
    characrers.append(["n", "н"])
    characrers.append(["o", "о"])
    characrers.append(["p", "п"])
    characrers.append(["q", "қ"])
    characrers.append(["r", "р"])
    characrers.append(["s", "с"])
    characrers.append(["t", "т"])
    characrers.append(["u", "у"])
    characrers.append(["v", "в"])
    characrers.append(["x", "х"])
    characrers.append(["y", "й"])
    characrers.append(["z", "з"])
    characrers.append(["А", "A"])
    characrers.append(["Б", "B"])
    characrers.append(["С", "C"])
    characrers.append(["Ч", "Ch"])
    characrers.append(["Д", "D"])
    characrers.append(["Е", "E"])
    characrers.append(["Ф", "F"])
    characrers.append(["Г", "G"])
    characrers.append(["Ҳ", "H"])
    characrers.append(["И", "I"])
    characrers.append(["Ж", "J"])
    characrers.append(["К", "K"])
    characrers.append(["Л", "L"])
    characrers.append(["М", "M"])
    characrers.append(["Н", "N"])
    characrers.append(["О", "O"])
    characrers.append(["П", "P"])
    characrers.append(["Қ", "Q"])
    characrers.append(["Р", "R"])
    characrers.append(["С", "S"])
    characrers.append(["Ш", "Sh"])
    characrers.append(["Т", "T"])
    characrers.append(["У", "U"])
    characrers.append(["В", "V"])
    characrers.append(["Х", "X"])
    characrers.append(["Й", "Y"])
    characrers.append(["Я", "Ya"])
    characrers.append(["Ю", "Yu"])
    characrers.append(["Ё", "Yo"])
    characrers.append(["З", "Z"])
    characrers.append(["Ғ", "Gʼ"])
    characrers.append(["а", "a"])
    characrers.append(["б", "b"])
    characrers.append(["с", "c"])
    characrers.append(["ч", "ch"])
    characrers.append(["д", "d"])
    characrers.append(["е", "e"])
    characrers.append(["ф", "f"])
    characrers.append(["г", "g"])
    characrers.append(["ҳ", "h"])
    characrers.append(["и", "i"])
    characrers.append(["ж", "j"])
    characrers.append(["к", "k"])
    characrers.append(["л", "l"])
    characrers.append(["м", "m"])
    characrers.append(["н", "n"])
    characrers.append(["о", "o"])
    characrers.append(["п", "p"])
    characrers.append(["қ", "q"])
    characrers.append(["р", "r"])
    characrers.append(["с", "s"])
    characrers.append(["ш", "sh"])
    characrers.append(["т", "t"])
    characrers.append(["у", "u"])
    characrers.append(["в", "v"])
    characrers.append(["х", "x"])
    characrers.append(["й", "y"])
    characrers.append(["я", "ya"])
    characrers.append(["ю", "yu"])
    characrers.append(["ё", "yo"])
    characrers.append(["з", "z"])
    characrers.append(["ғ", "gʼ"])

    characrers.append(["ъ", "`"])

    characrers.append(["`", "ъ"])
    characrers.append(["'", "ъ"])

    lotin = False
    arr = list(text)
    for ar in arr:
        if 0 < ord(ar) < 1024:
            lotin = True
        for obj in characrers:
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
    return render_template('login2.html')


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
