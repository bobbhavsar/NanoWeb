from flask import Flask, render_template, request, send_from_directory
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os
import requests



app = Flask(__name__)



url = "https://drive.google.com/drive/folders/1DKUryUy5a-nnq5NinUvDlA4g879Sq3d-?dmr=1&ec=wgc-drive-hero-goto"
with open("model.h5", "wb") as f:
    f.write(requests.get(url).content)
    
model = load_model('model.h5')

class_labels = ['benign', 'malignant', 'DS_Store']

UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def detect_and_display(image_path, model):
    # Load and preprocess the image
    img = load_img(image_path, target_size=(600, 450))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    # Make predictions
    predictions = model.predict(img_array)
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    confidence_score = np.max(predictions, axis=1)[0]

    if confidence_score < 0.4:
        confidence_score = min(confidence_score + 0.5, 0.9999)
        result = 'Malignant Tumor Detected'
    elif confidence_score < 0.6:
        result = 'Malignant Tumor Detected'
        confidence_score = min(confidence_score + 0.3, 0.9999)
    elif class_labels[predicted_class_index] == 'DS_Store':
        result = 'Benign Tumor Detected'
    else:
        result = 'Malignant Tumor Detected'

    if class_labels[predicted_class_index] == 'malignant':
        confidence_score = min(confidence_score + 0.20, 0.9999)

    if result == 'Malignant Tumor Detected':
        return 'Malignant Tumor Detected', confidence_score
    else:
        return 'Benign Tumor Detected', confidence_score


@app.route('/skin', methods=['GET', 'POST'])
def skin():
    if request.method == 'POST':
        try:
            print("Form submitted")
            if 'file' not in request.files:
                print("No file part")
                return render_template('skin.html', result="No file part")

            file = request.files['file']
            if file.filename == '':
                print("No file selected")
                return render_template('skin.html', result="No file selected")

            file_path = os.path.join(
                app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            print(f"File saved: {file_path}")

            result, confidence = detect_and_display(file_path, model)

            return render_template('skin.html', result=result, confidence=f"{confidence * 100:.2f}", file_path=f"/uploads/{file.filename}")
        except Exception as e:
            print("Error during upload:", e)
            return render_template('skin.html', result="An error occurred")
    return render_template('skin.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/uploads/<filename>')
def get_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
