from flask import Flask, request, jsonify, send_file, url_for
from PIL import Image
from werkzeug.utils import secure_filename
from datetime import datetime
from flask_cors import CORS, cross_origin
from create_mockups import create_mockups
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'swatches'
MOCKUP_FOLDER = 'mockups'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MOCKUP_FOLDER'] = MOCKUP_FOLDER
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/", methods=['GET'])
def welcome():
    return {
        "message": "Welcome to the Mockup Generator API."
    }


@app.route("/upload-images", methods=['POST'])
def upload_images():
    if 'images' not in request.files:
        return {
            "message": "No file part"
        }, 400
    
    images = request.files.getlist('images')
    image_urls = []
    image_name = []
    for image in images:
        if image.filename == '':
            return {
                "message": "No selected file"
            }, 400
        if image:
            filename = secure_filename(image.filename)
            image_name.append(filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_urls.append(url_for('get_image', filename=filename, _external=True))

    print(image_name)
    create_mockups(image_name)
    
    return {
        "message": "Images uploaded successfully.",
        "image_urls": image_urls
    }

@app.route('/images')
def get_images():
    images = []
    mockups_folder = 'mockups'
    
    # Check if the directory exists
    if os.path.exists(mockups_folder):
        for filename in os.listdir(mockups_folder):
            if os.path.isfile(os.path.join(mockups_folder, filename)):
                image_url = url_for('get_image', filename=filename, _external=True)
                images.append(image_url)
                
    return jsonify({
        "images": images
    })

@app.route('/images/<filename>')
def get_image(filename):
    mockups_folder = 'mockups'
    # check if the file exists
    if not os.path.exists(os.path.join(mockups_folder, filename)):
        return {
            "message": "Image not found."
        }, 404
    return send_file(os.path.join(mockups_folder, filename))

@app.route('/html')
def get_html():
    return send_file('index.html')

@app.route('/upload')
def get_upload():
    return send_file('upload_images.html')