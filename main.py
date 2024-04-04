
# from aiModelClass import AskChat
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from bson.objectid import ObjectId
import base64
# from aiAzureModel import AskAzure

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

@app.route('/api/pdfs', methods=['GET'])
def get_pdfs():
    # List all PDF files in the directory
    pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
    return jsonify(pdf_files)


@app.route('/pdfs/<path:filename>', methods=['GET'])
def serve_pdf(filename):
    # Ensure that the requested file is a PDF
    if not filename.lower().endswith('.pdf'):
        return "Not a PDF file", 400
    
    # Get the full path of the requested PDF file
    file_path = os.path.join(pdf_directory, filename)
    
    # Check if the file exists
    if not os.path.isfile(file_path):
        return "PDF not found", 404
    
    file = send_from_directory(pdf_directory, filename)
    
    # Serve the PDF file
    return file

@app.route("/users", methods=['GET'])
def get_all_users():
    users = list(db.users.find({}))

    for user in users:
        user['_id'] = str(user['_id'])

    return jsonify({"message": 'success', 'ok': True, 'users': users})



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


def read_pdf_content(pdf_path):
    pdf_content = ''
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            pdf_content += pdf_reader.pages[page_num].extract_text()
    return pdf_content


if __name__ == '__main__':
    app.run( port=5000, debug = True )