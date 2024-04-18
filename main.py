import os
from dotenv import load_dotenv
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import Utils
app = Flask(__name__)

load_dotenv()

ROUTE = os.environ.get("ROUTE")

utils = Utils()

CORS(app)

app.config['USERS_DOCUMENTS'] = 'Input Files'

@app.route('/extract', methods=['POST']) 
def extract_content():
    if 'images' not in request.files:
        return jsonify({'error': 'No PDF part'})

    images = request.files.getlist('images')

    response = []

    for image in images:

        image_path = os.path.join(app.config['USERS_DOCUMENTS'], image.filename)
        image.save(image_path)

        barcode = utils.getBarcodeFromImage(image.filename)

        with open(image_path, "rb") as img_file:
            image_data_base64 = base64.b64encode(img_file.read()).decode("utf-8")

        imageWithData = {
            "name": image.filename,
            "barcode": barcode,
            "image": image_data_base64
        }

        response.append(imageWithData)


    utils.delete_images(app.config['USERS_DOCUMENTS']) 
    return jsonify({'message': 'Images uploaded successfully', "ok": True, 'data': response})


if __name__ == '__main__':
    app.run( port=5000, debug = True )