from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageFilter
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# sharpen image
# def sharpen_image(input_image_path, output_image_path):
#     image = Image.open(input_image_path)
#     sharpened_image = image.filter(ImageFilter.SHARPEN)  
#     sharpened_image.save(output_image_path)

def convert_to_grayscale(input_image, output_image_path):
    image = Image.open(input_image)
    grayscale_image = image.convert("L")  
    grayscale_image.save(output_image_path)

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    upload_file = request.files['image']

    if upload_file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    filename = upload_file.filename
    upload_file.save(os.path.join(UPLOAD_FOLDER, filename))

    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_path = os.path.join(PROCESSED_FOLDER, filename)
    # sharpen_image(input_path, output_path)
    convert_to_grayscale(input_path, output_path)

    # JSON return
    processed_url = request.url_root + 'processed/' + filename
    return jsonify({'processed_image_url': processed_url}), 200


@app.route('/processed/<filename>')
def serve_processed_image(filename):
    return send_file(os.path.join(PROCESSED_FOLDER, filename))

if __name__ == '__main__':
    app.run(debug=True)



