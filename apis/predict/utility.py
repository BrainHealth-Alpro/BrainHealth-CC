from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

class Predict:
    def __init__(self):
        self.model = load_model('model.h5')
        self.class_mappings = {0: 'Glioma', 1: 'Meningioma', 2: 'Notumor', 3: 'Pituitary'}

    def load_and_preprocess_image(self, image_path, image_shape=(168, 168)):
        img = image.load_img(image_path, target_size=image_shape, color_mode='grayscale')
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
    
    def getPrediction(self, file):
        filepath = os.path.join('static', file.filename)
        file.save(filepath)
        img_array = self.load_and_preprocess_image(filepath)
        prediction = self.model.predict(img_array)
        predicted_label = self.class_mappings[np.argmax(prediction)]
        return predicted_label