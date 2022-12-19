import asyncio
import base64
import datetime
import io
import os
import random
import shutil
import sqlite3
import string
import time
import traceback
import urllib
import uuid
import yaml

import flask
import imutils
import numpy
import numpy as np
from PIL import Image, ImageChops, ImageFile
# from cv2 import cv2
import cv2
import urllib3
from pysitemap import crawler
from skimage.metrics import structural_similarity as compare_ssim
from flask import render_template, request, jsonify, flash, send_file, send_from_directory, abort, session
from sqlalchemy import func, desc
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import functions
from werkzeug.utils import secure_filename
import googletrans
from googletrans import Translator
import pyttsx3

from website import app, ALLOWED_EXTENSIONS, GET_FILE_FORMATS, db, youtube_downloader, file_converter, TWILIO_ACCOUNT_SID, \
    TWILIO_API_KEY_SID, TWILIO_API_KEY_SECRET, socketio, instagram_downloader

import json

from website.models import Users, Chat, ChatMessage, ChatUserRelation, UserSchema, ChatUserRelationSchema, user_schema, \
    users_schema, chat_user_relations_schema, chat_messages_schema, chat_message_schema
import pytube
import twilio.jwt.access_token
import twilio.jwt.access_token.grants
import twilio.rest
from flask_socketio import SocketIO, send, emit, join_room, leave_room

from website.white_box_cartoonizer.cartoonize import WB_Cartoonize
import skvideo
import skvideo.io
skvideo.setFFmpegPath(r'C:\Python310\Lib\site-packages\ffmpeg')
account_sid = TWILIO_ACCOUNT_SID
api_key = TWILIO_API_KEY_SID
api_secret = TWILIO_API_KEY_SECRET
twilio_client = twilio.rest.Client(api_key, api_secret, account_sid)

with open('./website/config.yaml', 'r') as fd:
    opts = yaml.safe_load(fd)
if opts['colab-mode']:
    from flask_ngrok import run_with_ngrok  # to run the application on colab using ngrok

if not opts['run_local']:
    if 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
        from website.gcloud_utils import upload_blob, generate_signed_url, delete_blob, download_video
    else:
        raise Exception("GOOGLE_APPLICATION_CREDENTIALS not set in environment variables")
    from website.video_api import api_request
    # Algorithmia (GPU inference)
if opts['colab-mode']:
    run_with_ngrok(app)  # starts ngrok when the app is run

app.config['UPLOAD_FOLDER_VIDEOS'] = 'website/static/uploaded_videos'
app.config['CARTOONIZED_FOLDER'] = 'website/static/cartoonized_images'

app.config['OPTS'] = opts


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/yandex_6bd5e2cc7d84e7b1.html')
def send_yandex_verification():
    return send_from_directory(app.template_folder, 'yandex_6bd5e2cc7d84e7b1.html')


@app.route('/googleed00602540a61448.html')
def send_google_verification():
    return send_from_directory(app.template_folder, 'googleed00602540a61448.html')


@app.route('/zen_7l9bCOKi66HKyY4ilLYmulKUQTlrZLJrS3HSjTiMhq0GoD4ap8COxE7Bjw1oYf26.html')
def send_zen_verification():
    return send_from_directory(app.template_folder,
                               'zen_7l9bCOKi66HKyY4ilLYmulKUQTlrZLJrS3HSjTiMhq0GoD4ap8COxE7Bjw1oYf26.html')


@app.route('/sitemap.xml')
def send_sitemap():
    return send_from_directory(app.static_folder, 'sitemap.xml')


@app.route('/BingSiteAuth.xml')
def send_bing_site_auth():
    return send_from_directory(app.static_folder, 'BingSiteAuth.xml')


@app.route('/rss.xml')
def send_rss():
    return send_from_directory(app.static_folder, 'rss.xml')


@app.route('/app-ads.txt')
def send_adstxt():
    return send_from_directory(app.static_folder, 'app-ads.txt')


@app.route('/robots.txt')
def send_robots():
    return send_from_directory(app.static_folder, 'robots.txt')


@app.route('/terms')
def terms():
    return render_template('terms.html')


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


@app.route("/password_generator", methods=['GET', 'POST'])
def password_generator():
    if request.method == 'GET':
        return render_template('password_generator.html')
    if request.method == 'POST':
        characterList = ""
        json_data = request.json
        PasswordLength = int(json_data['PasswordLength'])
        Uppercase = json_data['Uppercase']
        Lowercase = json_data['Lowercase']
        Numbers = json_data['Numbers']
        Symbols = json_data['Symbols']
        if Uppercase:
            characterList += string.ascii_uppercase
        if Lowercase:
            characterList += string.ascii_lowercase
        if Numbers:
            characterList += string.digits
        if Symbols:
            characterList += string.punctuation
        password = []

        for i in range(PasswordLength):
            # Picking a random character from our
            # character list
            randomchar = random.choice(characterList)

            # appending a random character to password
            password.append(randomchar)
        return {"result": "".join(password)}


@app.route("/sitemap", methods=['GET', 'POST'])
def sitemap():
    if request.method == 'GET':
        return render_template('sitemap.html')
    if request.method == 'POST':
        url = request.args.get('url')
        from asyncio import events, windows_events
        el = windows_events.ProactorEventLoop()
        events.set_event_loop(el)
        crawler(url, out_file='sitemap.xml', exclude_urls=[".ico", ".css", ".pdf", ".jpg", ".zip", ".png", ".svg"])
        basedir = os.path.abspath(os.path.dirname(__file__))
        time.sleep(10)
        return {"result": os.path.join(basedir.replace('\\website', ''), 'sitemap.xml')}


@app.route('//.well-known/pki-validation/057563D5748D2753B84E7944B00F213F.txt')
def send_ssl():
    return send_from_directory(app.static_folder, '057563D5748D2753B84E7944B00F213F.txt')


# region online services
wb_cartoonizer = WB_Cartoonize(os.path.abspath("website/white_box_cartoonizer/saved_models/"), opts['gpu'])


def convert_bytes_to_image(img_bytes):
    """Convert bytes to numpy array

    Args:
        img_bytes (bytes): Image bytes read from flask.

    Returns:
        [numpy array]: Image numpy array
    """

    pil_image = Image.open(io.BytesIO(img_bytes))
    if pil_image.mode == "RGBA":
        image = Image.new("RGB", pil_image.size, (255, 255, 255))
        image.paste(pil_image, mask=pil_image.split()[3])
    else:
        image = pil_image.convert('RGB')
    image = np.array(image)

    return image


@app.route('/')
@app.route('/cartoonize', methods=["POST", "GET"])
def cartoonize():
    opts = app.config['OPTS']
    if flask.request.method == 'POST':
        try:
            if flask.request.files.get('image'):
                img = flask.request.files["image"].read()

                ## Read Image and convert to PIL (RGB) if RGBA convert appropriately
                image = convert_bytes_to_image(img)

                img_name = str(uuid.uuid4())

                cartoon_image = wb_cartoonizer.infer(image)

                cartoonized_img_name = os.path.join(app.config['CARTOONIZED_FOLDER'], img_name + ".jpg")
                cv2.imwrite(cartoonized_img_name, cv2.cvtColor(cartoon_image, cv2.COLOR_RGB2BGR))

                if not opts["run_local"]:
                    # Upload to bucket
                    output_uri = upload_blob("cartoonized_images", cartoonized_img_name, img_name + ".jpg",
                                             content_type='image/jpg')
                    print(output_uri)
                    # Delete locally stored cartoonized image
                    os.system("rm " + cartoonized_img_name)
                    cartoonized_img_name = generate_signed_url(output_uri)
                print(cartoonized_img_name)
                return render_template("index_cartoonized.html",
                                       cartoonized_image=cartoonized_img_name.replace('website/', ''))

            if flask.request.files.get('video'):

                filename = str(uuid.uuid4()) + ".mp4"
                video = flask.request.files["video"]
                original_video_path = os.path.join(app.config['UPLOAD_FOLDER_VIDEOS'], filename)
                video.save(original_video_path)

                modified_video_path = os.path.join(app.config['UPLOAD_FOLDER_VIDEOS'],
                                                   filename.split(".")[0] + "_modified.mp4")

                ## Fetch Metadata and set frame rate
                file_metadata = skvideo.io.ffprobe(original_video_path)
                original_frame_rate = None
                if 'video' in file_metadata:
                    if '@r_frame_rate' in file_metadata['video']:
                        original_frame_rate = file_metadata['video']['@r_frame_rate']

                if opts['original_frame_rate']:
                    output_frame_rate = original_frame_rate
                else:
                    output_frame_rate = opts['output_frame_rate']

                output_frame_rate_number = int(output_frame_rate.split('/')[0])

                # change the size if you want higher resolution :
                ############################
                # Recommnded width_resize  #
                ############################
                # width_resize = 1920 for 1080p: 1920x1080.
                # width_resize = 1280 for 720p: 1280x720.
                # width_resize = 854 for 480p: 854x480.
                # width_resize = 640 for 360p: 640x360.
                # width_resize = 426 for 240p: 426x240.
                width_resize = opts['resize-dim']

                # Slice, Resize and Convert Video as per settings
                if opts['trim-video']:
                    # change the variable value to change the time_limit of video (In Seconds)
                    time_limit = opts['trim-video-length']
                    if opts['original_resolution']:
                        os.system(
                            "ffmpeg -hide_banner -loglevel warning -ss 0 -i '{}' -t {} -filter:v scale=-1:-2 -r {} -c:a copy '{}'".format(
                                os.path.abspath(original_video_path), time_limit, output_frame_rate_number,
                                os.path.abspath(modified_video_path)))
                    else:
                        os.system(
                            "ffmpeg -hide_banner -loglevel warning -ss 0 -i '{}' -t {} -filter:v scale={}:-2 -r {} -c:a copy '{}'".format(
                                os.path.abspath(original_video_path), time_limit, width_resize,
                                output_frame_rate_number, os.path.abspath(modified_video_path)))
                else:
                    if opts['original_resolution']:
                        os.system(
                            "ffmpeg -hide_banner -loglevel warning -ss 0 -i '{}' -filter:v scale=-1:-2 -r {} -c:a copy '{}'".format(
                                os.path.abspath(original_video_path), output_frame_rate_number,
                                os.path.abspath(modified_video_path)))
                    else:
                        os.system(
                            "ffmpeg -hide_banner -loglevel warning -ss 0 -i '{}' -filter:v scale={}:-2 -r {} -c:a copy '{}'".format(
                                os.path.abspath(original_video_path), width_resize, output_frame_rate_number,
                                os.path.abspath(modified_video_path)))

                audio_file_path = os.path.join(app.config['UPLOAD_FOLDER_VIDEOS'],
                                               filename.split(".")[0] + "_audio_modified.mp4")
                os.system(
                    "ffmpeg -hide_banner -loglevel warning -i '{}' -map 0:1 -vn -acodec copy -strict -2  '{}'".format(
                        os.path.abspath(modified_video_path), os.path.abspath(audio_file_path)))

                if opts["run_local"]:
                    cartoon_video_path = wb_cartoonizer.process_video(modified_video_path, output_frame_rate)
                else:
                    data_uri = upload_blob("processed_videos_cartoonize", modified_video_path, filename,
                                           content_type='video/mp4', algo_unique_key='cartoonizeinput')
                    response = api_request(data_uri)
                    # Delete the processed video from Cloud storage
                    delete_blob("processed_videos_cartoonize", filename)
                    cartoon_video_path = download_video('cartoonized_videos', os.path.basename(response['output_uri']),
                                                        os.path.join(app.config['UPLOAD_FOLDER_VIDEOS'],
                                                                     filename.split(".")[0] + "_cartoon.mp4"))

                ## Add audio to the cartoonized video
                final_cartoon_video_path = os.path.join(app.config['UPLOAD_FOLDER_VIDEOS'],
                                                        filename.split(".")[0] + "_cartoon_audio.mp4")
                os.system("ffmpeg -hide_banner -loglevel warning -i '{}' -i '{}' -codec copy -shortest '{}'".format(
                    os.path.abspath(cartoon_video_path), os.path.abspath(audio_file_path),
                    os.path.abspath(final_cartoon_video_path)))

                # Delete the videos from local disk
                os.system("rm {} {} {} {}".format(original_video_path, modified_video_path, audio_file_path,
                                                  cartoon_video_path))

                return render_template("index_cartoonized.html", cartoonized_video=final_cartoon_video_path)

        except Exception:
            print(traceback.print_exc())
            flash("Our server hiccuped :/ Please upload another file! :)")
            return render_template("index_cartoonized.html")
    else:
        return render_template("index_cartoonized.html")


@app.route("/instagram_downloader", methods=['GET', 'POST'])
def instagram_downloader_():
    if request.method == 'GET':
        return render_template('instagram_downloader.html')
    if request.method == 'POST':
        json_data = request.json
        user_name = json_data['user_name']
        if user_name is None:
            return {"result": "0"}
        else:
            result = instagram_downloader.save_insta_collection(user_name)
            basedir = os.path.abspath(os.path.dirname(__file__))
            print(basedir)
            if result == user_name and os.path.exists(basedir.replace('website', result)):
                shutil.make_archive(result, 'zip', basedir.replace('website', result))
                now = time.time()
                future = now + 3
                while True:
                    print(future)
                    if time.time() > future:
                        return {"result": basedir.replace('website', result) + '.zip'}
            else:
                return {"result": "0"}


@app.route("/youtube_downloader", methods=['GET', 'POST'])
def youtube_downloader_():
    if request.method == 'GET':
        return render_template('youtube_downloader.html')
    if request.method == 'POST':
        json_data = request.json
        choice = json_data['choice']
        quality = json_data['quality']  # low, medium, high, very high
        link = json_data['link']
        if link[0:23] == "https://www.youtube.com" or link[0:19] == "https://youtube.com" or link[
                                                                                             0:16] == "https://youtu.be":
            if choice == 1 or choice == 2:
                if choice == 2:
                    print("Pleylist yuklab olinmoqda...")
                    filenames = youtube_downloader.download_playlist(link, quality)
                    print("Yuklab olish tugadi!")
                    print(filenames)
                if choice == 1:
                    filename = youtube_downloader.download_video(link, quality)
                    result = app.root_path.replace('website', '') + filename
                    print(result)
                    return {"result": result}
            elif choice == 3:
                print("Yuklab olinmoqda...")
                filename = youtube_downloader.download_video(link, 'low')
                print("Oʻzgartirilmoqda...")
                file_converter.convert_to_mp3(filename)
                result = app.root_path.replace('website', '') + filename.replace('.mp4', '.mp3')
                return {"result": result}
            else:
                print("Yaroqsiz kiritish! Tugatilmoqda...")
        else:
            return {"result": "0"}


@app.route("/send_file")
def send_file_():
    filename = request.args.get('filename')
    if filename[-4:] in GET_FILE_FORMATS:
        return send_file(filename, as_attachment=True)
    else:
        return send_file('C:\\inetpub\\pythonProject_complexprogrammer_web\\website\\static\\img\\fuck.jpg', as_attachment=True)


@app.route("/remove_file", methods=['POST'])
def remove_file_():
    filename = request.args.get('filename')
    if os.path.exists(filename) and filename[-4:] in GET_FILE_FORMATS:
        if filename[-4:] == ".mp3":
            filename_ = filename[:-4] + ".mp4"
            if os.path.exists(filename_):
                os.remove(filename_)
        if filename[-4:] == ".zip":
            filename_ = filename[:-4]
            path = filename_
            shutil.rmtree(path, ignore_errors=True)
            # for file_name in os.listdir(path):
            #     print(file_name)
            #     file = path + file_name
            #     print(file)
            #     if os.path.isfile(file):
            #         print('Deleting file:', file)
            #         os.remove(file)
        os.remove(filename)
        return "1"
    else:
        return "0"


# @app.route("/video_chat")
# def video_chat():
#     return render_template('video_chat.html')
#
#
# @app.route("/join-room", methods=["POST"])
# def join_room():
#     username = request.get_json(force=True).get('username')
#     if not username:
#         abort(401)
#
#     token = twilio.AccessToken(account_sid, api_key,
#                                api_secret, identity=username)
#     token.add_grant(twilio.VideoGrant(room='My Room'))
#
#     return {'token': token.to_jwt().decode()}


def find_or_create_room(room_name):
    try:
        # try to fetch an in-progress room with this name
        twilio_client.video.rooms(room_name).fetch()
    except twilio.base.exceptions.TwilioRestException:
        # the room did not exist, so create it
        twilio_client.video.rooms.create(unique_name=room_name, type="go")


def get_access_token(room_name):
    # create the access token
    access_token = twilio.jwt.access_token.AccessToken(
        account_sid, api_key, api_secret, identity=uuid.uuid4().int
    )
    # create the video grant
    video_grant = twilio.jwt.access_token.grants.VideoGrant(room=room_name)
    # Add the video grant to the access token
    access_token.add_grant(video_grant)
    return access_token


@app.route("/exchangerates")
def exchangerates():
    return render_template('exchangerates.html')


@app.route("/GetExchangeRates", methods=['GET'])
def GetExchangeRates():
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
    user = Users.query.filter_by(uid=uid).first()
    if user is None:
        user = Users(photo_url=photo_url, name=name, email=email, phone=phone, provider_id=provider_id, uid=uid,
                     email_verified=email_verified, created_date=datetime.datetime.now(),
                     login_date=datetime.datetime.now(), login_count=1, active=1)
        db.session.add(user)
        db.session.commit()
    else:
        user.login_date = datetime.datetime.now()
        user.login_count = user.login_count + 1
        user.active = 1
        db.session.commit()
    session.permanent = True
    session['user_id'] = user.id
    session['room'] = 'ComplexProgrammerChat'
    return jsonify(user_schema.dump(user))


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

    return jsonify(users_schema.dump(user))


@app.route("/getMyContacts", methods=['POST'])
def getMyContacts():
    user_id = request.args.get('user_id')
    user = Users.query.filter(Users.id != user_id).all()
    print(users_schema.dump(user))
    return jsonify(users_schema.dump(user))


@socketio.on('join', namespace='/chat')
def join(message):
    room = session.get('room')
    if room is not None:
        join_room(room)
        emit('status', {'sender_id': session.get('user_id'), 'text': str(room) + '  contected', 'active': True}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    user_id = session.get('user_id')
    room = session.get('room')
    session.clear()
    emit('status', {'sender_id': user_id, 'text': str(room) + ' disconnected', 'active': False}, room=room)
    leave_room(room)


@app.route("/getCountNewMessages", methods=['POST'])
def getCountNewMessages():
    user_id = request.args.get('user_id')
    chat_user_relation = ChatUserRelation.query.filter(ChatUserRelation.user_id == user_id,
                                                       ChatUserRelation.is_deleted == False).order_by(
        ChatUserRelation.id).all()
    chat_ids = []
    for item in chat_user_relation:
        chat_ids.append(item.chat_id)
    result = ChatUserRelation.query.filter(ChatUserRelation.chat_id.in_(chat_ids),
                                                       ChatUserRelation.user_id != user_id)\
        .with_entities(
        func.sum(ChatUserRelation.count_new_message).label("mySum")
    ).first()
    return jsonify(result.mySum)


@app.route("/getChatUserRelations", methods=['POST'])
def getChatUserRelations():
    user_id = request.args.get('user_id')
    chat_user_relation = ChatUserRelation.query.filter(ChatUserRelation.user_id == user_id,
                                                       ChatUserRelation.is_deleted == False).order_by(
        ChatUserRelation.id).all()
    chat_ids = []
    for item in chat_user_relation:
        chat_ids.append(item.chat_id)
    chat_user_relation = ChatUserRelation.query.filter(ChatUserRelation.chat_id.in_(chat_ids),
                                                       ChatUserRelation.user_id != user_id).join(Chat).join(ChatMessage)\
        .order_by(desc(ChatMessage.created_date)).all()
    print(chat_user_relations_schema.dump(chat_user_relation))
    return jsonify(chat_user_relations_schema.dump(chat_user_relation))


@app.route('/getChatMessagesByChatId', methods=['POST'])
def getChatMessagesByChatId():
    chat_id = request.args.get('chat_id')
    chat_message = ChatMessage.query.filter(
        ChatMessage.chat_id == chat_id).order_by(
        ChatMessage.id).all()
    return jsonify(chat_messages_schema.dump(chat_message))


@app.route('/getChatMessages', methods=['POST'])
def getChatMessages():
    sender_id = request.args.get('sender_id')
    receiver_id = request.args.get('receiver_id')
    chat_user_relation1 = ChatUserRelation.query.filter(ChatUserRelation.user_id == receiver_id,
                                                        ChatUserRelation.is_deleted == False).order_by(
        ChatUserRelation.id).all()
    chat_user_relation2 = ChatUserRelation.query.filter(ChatUserRelation.user_id == sender_id,
                                                        ChatUserRelation.is_deleted == False).order_by(
        ChatUserRelation.id).all()
    chat_ids1 = []
    for item in chat_user_relation1:
        chat_ids1.append(item.chat_id)
    chat_ids2 = []
    for item in chat_user_relation2:
        chat_ids2.append(item.chat_id)
    chat_id = common_data(chat_ids1, chat_ids2)
    print(chat_id)
    session['chat_id'] = chat_id
    chat_message = ChatMessage.query.filter(
        ChatMessage.chat_id == chat_id).order_by(
        ChatMessage.id).all()
    return jsonify(chat_messages_schema.dump(chat_message))


def common_data(list1, list2):
    for x in list1:
        for y in list2:
            if x == y:
                return x

    return 0


@app.route('/sendMessage', methods=['POST'])
def sendMessage():
    json_data = request.json
    print(json_data)
    sender_id = json_data['sender_id']
    receiver_id = json_data['receiver_id']
    text = json_data['text']
    chat_user_relation1 = ChatUserRelation.query.filter(ChatUserRelation.user_id == receiver_id,
                                                        ChatUserRelation.is_deleted == False).order_by(
        ChatUserRelation.id).all()
    chat_user_relation2 = ChatUserRelation.query.filter(ChatUserRelation.user_id == sender_id,
                                                        ChatUserRelation.is_deleted == False).order_by(
        ChatUserRelation.id).all()
    chat_ids1 = []
    for item in chat_user_relation1:
        chat_ids1.append(item.chat_id)
    chat_ids2 = []
    for item in chat_user_relation2:
        chat_ids2.append(item.chat_id)
    chat_id = common_data(chat_ids1, chat_ids2)
    if chat_id == 0:
        chat = Chat(type=0, created_by=sender_id, created_date=datetime.datetime.now())
        db.session.add(chat)
        db.session.commit()
        chat_message = ChatMessage(chat_id=chat.id, type=1, text=text, sender_id=sender_id, created_by=sender_id,
                                   created_date=datetime.datetime.now())
        db.session.add(chat_message)
        chat_user_relation = ChatUserRelation(user_id=sender_id, chat_id=chat.id, count_new_message=0)
        db.session.add(chat_user_relation)
        chat_user_relation = ChatUserRelation(user_id=receiver_id, chat_id=chat.id, count_new_message=1)
        db.session.add(chat_user_relation)
        db.session.commit()
    else:
        chat = Chat.query.filter_by(id=chat_id).first()
        chat.last_modified_by = sender_id
        chat.last_modified_date = datetime.datetime.now()
        chat_message = ChatMessage(chat_id=chat_id, type=1, text=text, sender_id=sender_id, created_by=sender_id,
                                   created_date=datetime.datetime.now())
        db.session.add(chat_message)
        db.session.commit()
        chat_user_relation = ChatUserRelation.query.filter_by(chat_id=chat_id, user_id=receiver_id).first()
        chat_user_relation.count_new_message = chat_user_relation.count_new_message + 1
        db.session.commit()
        # db.session.close_all()
        emit('message', {'sender_id': session.get('user_id'), 'chat_id': chat.id, 'created_date': str(chat_message.created_date), 'text': text}, room=session.get('room'), namespace='/chat')
    return jsonify(chat_message_schema.dump(chat_message))


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
