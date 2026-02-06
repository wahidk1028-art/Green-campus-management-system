import cv2
import numpy as np
from tensorflow.keras.models import load_model

model = load_model('waste_classifier.h5')
classes = ['metal', 'paper', 'plastic']

IMG_SIZE = 150

def predict_waste(frame):
    img = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))
    img = img / 255.0
    img = np.reshape(img, (1, IMG_SIZE, IMG_SIZE, 3))

    prediction = model.predict(img)
    return classes[np.argmax(prediction)]
