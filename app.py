from flask import Flask, render_template, request
import numpy as np
import cv2
import time
from tensorflow.keras.models import load_model

app = Flask(__name__)

model = load_model("model.keras")

# Classes
classes = [
    'Pepper__bell___Bacterial_spot',
    'Pepper__bell___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Tomato_Bacterial_spot',
    'Tomato_Early_blight',
    'Tomato_Late_blight',
    'Tomato_Leaf_Mold',
    'Tomato_Septoria_leaf_spot',
    'Tomato_Spider_mites_Two_spotted_spider_mite',
    'Tomato__Target_Spot',
    'Tomato__Tomato_YellowLeaf__Curl_Virus',
    'Tomato__Tomato_mosaic_virus',
    'Tomato_healthy'
]

# Clean label (nice UI)
def clean_label(label):
    return label.replace("_", " ").replace("___", " - ")

def predict_image(path):
    img = cv2.imread(path)
    img = cv2.resize(img, (128,128))
    img = img / 255.0
    img = np.reshape(img, (1,128,128,3))

    pred = model.predict(img)[0]   # 🔥 important

    # Main prediction
    index = np.argmax(pred)
    confidence = round(pred[index] * 100, 2)

    # Top 3 predictions
    top3_idx = pred.argsort()[-3:][::-1]

    top3 = []
    for i in top3_idx:
        top3.append({
            "name": clean_label(classes[i]),
            "conf": round(pred[i] * 100, 2)
        })

    return clean_label(classes[index]), confidence, top3


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['image']
        
        filename = str(int(time.time())) + file.filename
        filepath = "static/" + filename
        file.save(filepath)

        result, conf, top3 = predict_image(filepath)

        return render_template(
            'result.html',
            prediction=result,
            confidence=conf,
            top3=top3,
            img_path=filepath
        )

    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)