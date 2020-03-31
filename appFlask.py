import os
from flask import Flask, request, redirect, url_for,flash
from werkzeug.utils import secure_filename

from keras.models import Sequential, load_model
import keras,sys
import numpy as np
from PIL import Image

classes = ["budgerigar","cat","dog","hamster","rabbit"]
num_classes = len(classes)
image_size = 50

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('ファイルがありません')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            model = load_model('./pet_cnn_flask.h5')

            image = Image.open(filepath)
            image = image.convert('RGB')
            image = image.resize((image_size, image_size))
            data = np.asarray(image)
            X = []
            X.append(data)
            X = np.array(X)

            result = model.predict([X])[0]
            predicted = result.argmax()
            percentage = int(result[predicted] * 100)

            return "ラベル： " + classes[predicted] + ", 確率："+ str(percentage) + " %"


            #return redirect(url_for('uploaded_file', filename=filename))
    return '''
    <!doctype html>
    <html>
    <head>
    <meta charset="UTF-8">
    <title>画像判定システム</title>
    <link rel=stylesheet href=../bootstrap/bootstrap.css>
    <link rel=stylesheet href=appFlask.css></head>
    <body>
    <h1>画像判定システム</h1>
    <p>budgerigar(インコ)、cat(猫)、dog(犬)、hamster(ハムスター)、rabbit(ウサギ)の五種類の動物を学習させています。</p>
    <br><p>画像ファイルを入れることで％表示で何の動物の写真か当てられます。</p>
    <form method = post enctype = multipart/form-data>
    <label for=file>画像ファイルを選択</label><br>
    <input type=file name=file class=btn btn-special style=background-color:aqua;>
    <input type=submit value=判定 class=btn btn-special style=background-color:red;>
    </form>
    <script src=../bootstrap/jquery-3.4.1.js></script>
    <script src=../bootstrap/bootstrap.js></script>
    </body>
    </html>
    '''

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
