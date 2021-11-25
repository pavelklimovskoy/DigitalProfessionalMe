# -*- coding: utf-8 -*-
import os
from flask import Flask, jsonify, request, send_from_directory, render_template
from flask_cors import CORS, cross_origin
import codecs

import ParseModules
from ParseModules import *
from LoadModules import loadPage
from Logger import log

app = Flask(__name__)
CORS(app)

@app.route('/testHH')
def testHH():
    url = "https://taganrog.hh.ru/resume/79efe7160005df35640039ed1f456874554268"

    loadPage(url)

    return """
    <h1>Hello world!</h1>

    <iframe src="/templates/79efe7160005df35640039ed1f456874554268.html" width="853" height="480" frameborder="0" allowfullscreen></iframe>
    """

# Получение загруженной страницы по id
@app.route("/templates/<id>")
def pageFormHH(id):
    filename = id + ".html"
    return render_template(filename)

@app.route('/video')
def video():

    return """
    <h1>Hello world!</h1>

    <iframe src="https://hh.ru/employer" width="853" height="480" frameborder="0" allowfullscreen></iframe>
    """

@app.after_request
def apply_caching(response):
    response.headers["X-Frame-Options"] = "ALLOW"
    return response

@app.route("/inc")
def inc():
    file = open("count")
    k = int(file.read()) + 1
    file.close()
    file = open("count", "w")
    file.write(str(k))
    file.close()
    return str(k)

# Основная страница
@app.route("/")
def renderHtml():
    return render_template('index.html')

# Выдача скриптов
@app.route("/script")
def drawJS():
    return render_template('script.js')

# Смена поискового слова
@app.route('/newFindWord/<newWord>', methods=['GET'])
def changeFindWord(newWord):
    file = open("FindWord.txt", "w")
    file.write(newWord)
    file.close()
    return "Word changed"

# Получение поискового слова
@app.route("/getFindWord", methods=['GET'])
def getFindWord():
    if request.method == 'GET':
        file = open("FindWord.txt")
        word = file.read()
        file.close()
        return word

# Получение старница для парсинга
@app.route("/getPageForParse", methods=['GET'])
def pageForParse():
    if request.method == 'GET':
        return "https://rostov.hh.ru/resume/87f32e4d000339c37e0039ed1f4d496b635065"

# Получение старница для парсинга
@app.route("/reqForParse/<id>", methods=['GET'])
def reqForParse(id):
    if request.method == 'GET':
        filename = "templates/" + id + ".html"

        url = "https://hh.ru/resume/" + id

        response = urllib.request.urlopen(url)
        webContent = response.read().decode('utf-8')

        f = codecs.open(filename, "w", "utf-8")
        f.write(webContent)
        f.close

        return "https://taganrog.hh.ru/resume/" + id + " загружено"

# Выдача иконки
@app.route("/favicon.ico")
def favicon():
    log("favicon")
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    app.run(debug=True, port=80)
    counter = 0