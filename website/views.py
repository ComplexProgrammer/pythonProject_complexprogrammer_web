import os
import sqlite3
import urllib
from flask import render_template, request, jsonify
from website import app
from website.models import savollar
from website import db
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
    url = "http://195.158.6.195:4444/Api/C0mplexApi/GetExchangeRates"
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


@app.route("/avtotest/<id>")
def avtotest(id=0):
    return render_template('avtotest.html',bilet=id)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route("/GetSavol", methods=['GET'])
def GetSavol():
    id = request.args.get('id')
    bilet = request.args.get('bilet')
    conn = sqlite3.connect('website/avtotest.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    savol = cur.execute('SELECT * FROM savollar where bilet=="'+bilet+'" and raqam=='+id+';').fetchone()
    return jsonify(savol)


# endregion


#region online games
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
