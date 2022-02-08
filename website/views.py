import urllib
from flask import render_template
from website import app
import json


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route("/ExchangeRates")
def GetExchangeRates():
    url = "http://172.20.0.31:4444/Api/C0mplexApi/GetExchangeRates"
    response = urllib.request.urlopen(url)
    data = response.read()
    return render_template('ExchangeRates.html', data=json.loads(data), index=0)


