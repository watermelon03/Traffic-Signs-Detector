import sys
import cv2
import numpy as np
import json
import torch

def get_model_yolov5(img, model):
    # config model 
    model.conf = 0.40  # confidence threshold (0-1)
    model.iou = 0.45  # NMS IoU threshold (0-1)
    model.classes = None  # (optional list) filter by class, i.e. = [0, 15, 16] for persons, cats and dogs

    # Inference
    results = model(img)
    return np.squeeze(results.render())


text = sys.argv[1]
image_path = sys.argv[2]
model_json = sys.argv[3]

# Convert the model JSON string to a dictionary
model_dict = json.loads(model_json)
# Load the PyTorch model
model = torch.load(model_dict)

#Convert image to grayscale
image = cv2.imread(image_path)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

gray_image = get_model_yolov5(gray_image, model)
file_name = "gray_image.jpg"

cv2.imwrite(file_name, gray_image)

#Convert text to uppercase
text = text.upper()

# Create a JSON object
response = {
    "text": [
        {"number": 1,"main_text": text, "id": 69},
        {"number": 2,"main_text": "NAMOE", "id": 1412}
        ],
    "image_path": file_name
    }

# Send the JSON object back to the Node.js backend
print(json.dumps(response))