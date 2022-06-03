import os
from flask import Flask, jsonify, request, send_from_directory, render_template, json, make_response, redirect,\
    url_for, flash, send_file
from flask_cors import CORS, cross_origin
import flask_login
from flask_mongoengine import MongoEngine
import codecs
from jsonConvert import json_convert
from rchilli import rchilli_parse
from werkzeug.utils import secure_filename
import os

# Flask config
app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'test1',
    'host': '127.0.0.1',
    'port': 27017
}
app.config['JSON_AS_ASCII'] = False
app.config['UPLOAD_FOLDER'] = './static/data/cv/'
app.config.from_object(__name__)
CORS(app)


# MongoDb
db = MongoEngine()
db.init_app(app)

class User(db.Document):
    name = db.StringField()
    email = db.StringField()

    def to_json(self):
        return {"name": self.name,
                "email": self.email}

@app.route('/show', methods=['GET'])
def query_records():
    name = request.args.get('name')
    user = User.objects(name=name).first()

    if not user:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(user.to_json())

@app.route('/add', methods=['POST'])
def create_record():
    record = json.loads(request.data)
    user = User(name=record['name'],
                email=record['email'])
    user.save()

    return jsonify(user.to_json())

@app.route('/upd', methods=['POST'])
def update_record():
    record = json.loads(request.data)
    user = User.objects(name=record['name']).first()

    if not user:
        return jsonify({'error': 'data not found'})
    else:
        user.update(email=record['email'])

    return jsonify(user.to_json())

@app.route('/delete', methods=['POST'])
def delete_record():
    record = json.loads(request.data)
    user = User.objects(name=record['name']).first()

    if not user:
        return jsonify({'error': 'data not found'})
    else:
        user.delete()

    return jsonify(user.to_json())
# MongoDB


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        fname = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
        rchilli_parse(fname)
        converting(fname)
    return render_template('index.html', title='Digital Professional Me')


# Основная страница
@app.route('/')
def index():
    return render_template('index.html', title='Digital Professional Me')


# Основная страница
@app.route('/about')
def about_us():
    return render_template('aboutus.html', title='About us')


# Конвертация Json из формата Rchilli в формат, нужный для диаграммы
@app.route('/convert-<name>', methods=['GET'])
def converting(name):
    #args = request.args
    #jsonName = str(args.get('name'))
    #json_convert(jsonName)

    json_convert(name)
    return render_template('index.html')

@app.route('/getJson')
def get_json_data():
    path = './static/data/cv/rchilli.json'
    return send_file(path)

if __name__ == "__main__":
    #rchilli_parse('cv2.pdf')
    app.run(debug=True, port=5000, host="0.0.0.0")