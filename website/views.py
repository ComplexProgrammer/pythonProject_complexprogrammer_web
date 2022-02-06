from flask import render_template
from website import app


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/intro')
def intro_page():
    return render_template('intro.html')



