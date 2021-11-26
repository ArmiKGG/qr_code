import os
from flask import Flask, jsonify, make_response, render_template, request, flash, redirect, url_for
from flask_restful import reqparse, Api, Resource
from werkzeug.datastructures import FileStorage
from dotenv import load_dotenv
import cv2
import fitz
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = './tmp'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'


load_dotenv()

extensons_img = ['.jpg', '.png']


import os
if not os.path.exists('./tmp'):
    os.makedirs('./tmp')

def proces_path(path):
    try:
        img = cv2.imread(path)
        decoder = cv2.QRCodeDetector()
        data, points, _ = decoder.detectAndDecode(img)
        if points is not None:
            return {'decoded_url': data}
    except Exception as e:
        return {'error': e}


def convert_pdf_to_images(pdf_path):
    file_name = pdf_path.split('/')[-1]
    pdffile = pdf_path
    doc = fitz.open(pdffile)
    for i in range(doc.page_count - 1):
        page = doc.load_page(i)  # number of page
        pix = page.get_pixmap()
        output = fr"./tmp/{file_name} - {i}.png"
        pix.save(output)
        data = proces_path(output)
        return data


def get_qr(path_to_file):
    is_img = False
    for ext in extensons_img:
        if path_to_file.endswith(ext):
            is_img = True
    else:
        if_pdf = True
    if is_img:
        data = proces_path(path_to_file)
        if data:
            return data
        else:
            return {'error': 'unreadable img'}
    elif if_pdf:
        return convert_pdf_to_images(path_to_file)


def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/")
def home():
    return render_template('index.html')


@app.route('/api', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f"./tmp/{f.filename}")
        data = get_qr(f"./tmp/{f.filename}")
        for filename in os.listdir('./tmp'):
            if f.filename in filename:
                os.remove(f"./tmp/{filename}")
        return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    app.run(host="0.0.0.0")