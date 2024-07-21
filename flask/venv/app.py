from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image
import numpy as np
import os
import torch
import cv2
from ultralytics import YOLO
import io

app = Flask(__name__)
CORS(app)

#modelo YOLO
model = YOLO('C:/Users/johan/OneDrive/Escritorio/hackathon/best.pt')

@app.route('/detect', methods=['POST'])
def detect_microplastics():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    image = Image.open(file.stream)

    image = image.resize((640, 640), Image.LANCZOS)

    # Convertir la imagen a un formato compatible con el modelo
    img = np.array(image)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_tensor = torch.from_numpy(img_rgb).permute(2, 0, 1).float().unsqueeze(0) / 255.0

    # Realizar la detección
    results = model.predict(img_tensor)


    detected_objects = []
    for result in results:
        boxes = result.boxes
        data = boxes.data.cpu().numpy()

        for box in data:
            if len(box) >= 4:
                x1, y1, x2, y2 = box[:4]
                detected_objects.append({
                    'class': int(box[5]),
                    'confidence': float(box[4]),
                    'bbox': [float(x1), float(y1), float(x2), float(y2)]
                })

    # Procesar la imagen para visualizar detecciones
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    for obj in detected_objects:
        bbox = obj['bbox']
        cv2.rectangle(img_bgr, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (0, 255, 0), 2)

    # Convertir la imagen con detecciones a un objeto BytesIO
    output_img = io.BytesIO()
    _, img_encoded = cv2.imencode('.jpg', img_bgr)
    output_img.write(img_encoded.tobytes())
    output_img.seek(0)

    # Guardar la imagen temporalmente para servirla
    temp_filename = 'static/output.jpg'
    with open(temp_filename, 'wb') as f:
        f.write(img_encoded.tobytes())

    # Devolver la información de detección y la ruta de la imagen
    return jsonify({
        'detections': detected_objects,
        'num_objects': len(detected_objects),
        'image_path': f'/static/output.jpg' 
    })




if __name__ == '__main__':
    app.run(port=3500)




