import os
import sys 
from flask import (
    Flask, 
    request, 
    redirect, 
    url_for, 
    make_response, 
    jsonify, 
    render_template, 
    send_from_directory)

UPLOAD_FOLDER_ENTER = './image_enter'
UPLOAD_FOLDER_REFERENCE = './image_reference'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
        enter_images=os.listdir(UPLOAD_FOLDER_ENTER)[::-1],
        reference_images=os.listdir(UPLOAD_FOLDER_REFERENCE)[::-1])

@app.route('/upload', methods=['GET', 'POST'])
def uploads_file():
    # リクエストがポストかどうかの判別
    if request.method == 'POST':
        # ファイルがなかった場合の処理
        if 'upload_files' not in request.files:
            print("ファイルなし")
            return redirect(request.url)

        if request.files.getlist('upload_files')[0].filename:
            #画像オブジェクトを受け取る。
            uploads_files = request.files.getlist('upload_files')
            for uploads_file in uploads_files:
                #それぞれの画像に対してimage_enterまでのパスを定義作成してsaveメソッドを用いて保存する。
                img_path = os.path.join(UPLOAD_FOLDER_ENTER, uploads_file.filename)
                uploads_file.save(img_path)
        return redirect('/')

@app.route('/images/<path:path>')
def send_image(path):
    return send_from_directory(UPLOAD_FOLDER_ENTER, path)

#スクリプトからAPIを叩けるようにします。
if __name__ == "__main__":
    app.run(debug=True)