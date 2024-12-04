import os
from flask import Flask, request, redirect, render_template, flash
from werkzeug.utils import secure_filename
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Input, Dense, Dropout, BatchNormalization
from tensorflow.keras.preprocessing import image
from flask import Flask, current_app

import numpy as np


classes = ["猫","犬"]
image_size = 100

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif']) # アップロードを許可する拡張子
# from app import app
# from app import db
# with app.app_context():
#     db.create_all()
app = Flask(__name__)
current_app.name

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

model = load_model('./model.h5')#学習済みモデルをロード


@app.route('/', methods=['GET', 'POST'])
def upload_file(self):
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
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            filepath = os.path.join(UPLOAD_FOLDER, filename)

            #受け取った画像を読み込み、np形式に変換
            img = image.load_img(filepath, target_size=(image_size,image_size))
            img = image.img_to_array(img)
            data = np.array([img])
            #変換したデータをモデルに渡して予測する
            result = model.predict(data)[0]
            predicted = result.argmax()
            pred_answer = "これは" + classes[predicted] + " の写真です"

            return render_template("accounts/create.html",answer=pred_answer) # index.html側に犬猫の判定情報を渡す

    return render_template("accounts/create.html",answer="")

# 自PCでのチェック用
if __name__ == "__main__":
    app.run()

# # Render公開用
# if __name__ == "__main__":
#     port = int(os.environ.get('PORT', 8080))
#     app.run(host ='0.0.0.0',port = port)
