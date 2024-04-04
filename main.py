
import os
from dotenv import load_dotenv
import base64

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_pymongo import pymongo
from utils import Utils
app = Flask(__name__)

load_dotenv()

ROUTE = os.environ.get("ROUTE")

utils = Utils()

CORS(app)

CONNECTION_STRING_MONGODB = os.environ.get("CONNECTION_STRING_MONGODB")

client = pymongo.MongoClient(CONNECTION_STRING_MONGODB, tls=True, tlsAllowInvalidCertificates=True)
db = client.get_database('AiChat')

app.config['USERS_DOCUMENTS'] = '/Users/alexandreurluescu/Documents/current work/ScanBarcode-Project/ScanBarcode-WEB/server/Input Files'
 
pdf_directory = '/Users/alexandreurluescu/Documents/current work/CogNex/CogNex-BE/server/uploads'


@app.route('/extract', methods=['POST']) 
def extract_content():
    print(f"req {request.files}")
    if 'images' not in request.files:
        print('intra1')
        return jsonify({'error': 'No PDF part'})

    # pdfs = request.files.getlist('pdfs')
    images = request.files.getlist('images')
    # userId = request.form['userId']

    print('intra2')

    response = []

    for image in images:

        image_path = os.path.join(app.config['USERS_DOCUMENTS'], image.filename)
        image.save(image_path)

        print(f"image.filename {image.filename}")

        barcode = utils.getBarcodeFromImage(image.filename)

        with open(image_path, "rb") as img_file:
            image_data_base64 = base64.b64encode(img_file.read()).decode("utf-8")

        imageWithData = {
            "name": image.filename,
            "barcode": barcode,
            "image": image_data_base64
        }

        response.append(imageWithData)

        print(f"barcode {barcode}")


        
    return jsonify({'message': 'Images uploaded successfully', "ok": True, 'data': response})


if __name__ == '__main__':
    app.run( port=5000, debug = True )