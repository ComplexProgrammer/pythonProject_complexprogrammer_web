import urllib
from flask import render_template, request
from website import app
from website.models import ListTextValue
import json


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route("/ExchangeRates")
def ExchangeRates():
    return render_template('ExchangeRates.html')


@app.route("/GetExchangeRates", methods=['GET'])
def GetExchangeRates():
    url = "http://195.158.6.195:4444/Api/C0mplexApi/GetExchangeRates"
    request = urllib.request.urlopen(url)
    data = request.read()
    return { "data":json.loads(data)}



@app.route("/ChangeText", methods=['GET', 'POST'])
def ChangeText():
    print(request.form.get('old_text'))

    return render_template('ChangeText.html')


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
