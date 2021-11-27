import os
from flask import Flask, jsonify, make_response, render_template, request, flash, redirect, url_for
import cv2
import fitz
from pyzbar.pyzbar import decode

app = Flask(__name__)

UPLOAD_FOLDER = './tmp'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'


extensons_img = ['.jpg', '.png']


if not os.path.exists('./tmp'):
    os.makedirs('./tmp')
    
def second_method(img_path):
    data_src = decode(cv2.imread(img_path))
    link = str(data_src[0][0]).replace("b'", '').replace("'", '')
    return {'decoded_url': link}


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
        if data:
            return data
        else:
            data = second_method(output)
            if data:
                return data
        return {'error': 'unreadable pdf'}


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
            data = second_method(path_to_file)
            if data:
                return data
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
    app.run(host="0.0.0.0")
