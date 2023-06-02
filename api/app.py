from flask import Flask, request, jsonify
import cv2
import numpy as np
from os import path

darknet_route = path.abspath(path.join(__file__ ,"../../darknet"))

app = Flask(__name__)

semaphores = [
    {
        'id': 1,
        'name': 'Congreso 1000',
        'max_congestion': 150,
    },
    {
        'id': 2,
        'name': 'Santa Fe 8910',
        'max_congestion': 300,
    },
]

def get_object_count(file):

    # Load pre-trained YOLO model
    net = cv2.dnn.readNetFromDarknet(f'{darknet_route}/cfg/yolov3.cfg', f'{darknet_route}/yolov3.weights')

    # Read data/coco.names file and get class names
    with open(f'{darknet_route}/data/coco.names', 'r') as f:
        classes = [line.strip() for line in f.readlines()]


    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    # Preprocess image
    blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)

    # Set input for the network
    net.setInput(blob)

    # Forward pass through the network
    output_layers = net.getUnconnectedOutLayersNames()
    layer_outputs = net.forward(output_layers)

    # Initialize counters
    car_count = 0
    truck_count = 0
    bus_count = 0
    motorbike_count = 0

    # Process output detections
    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_index = np.argmax(scores)
            class_confidence = scores[class_index]

            confidence_threshold = 0.

            if class_confidence > confidence_threshold:
                predicted_class = classes[class_index]
                if predicted_class == 'car':
                    car_count += 1
                elif predicted_class == 'truck':
                    truck_count += 1
                elif predicted_class == 'bus':
                    bus_count += 1
                elif predicted_class == 'motorbike':
                    motorbike_count += 1

    # Create a dictionary with the counts
    counts = {
        'car': car_count,
        'truck': truck_count,
        'bus': bus_count,
        'motorbike': motorbike_count
    }

    return counts

@app.route('/detect-objects', methods=['POST'])
def detect_objects():
    # Get the image from the request
    file = request.files['image']

    # Get the counts
    counts = get_object_count(file)
    return jsonify(counts)


@app.route('/trigger/<int:id>', methods=['POST'])
def trigger(id):
    # Get the image from the request
    file = request.files['image']

    # Get the counts
    counts = get_object_count(file)


    # Get the semaphore
    semaphore = next((semaphore for semaphore in semaphores if semaphore['id'] == id), None)

    # Calculate the congestion
    should_trigger = (counts['car'] + counts['truck'] * 2 + counts['bus'] * 1.5 + counts['motorbike'] * 0.2) >= semaphore['max_congestion']

    return jsonify(should_trigger);



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
