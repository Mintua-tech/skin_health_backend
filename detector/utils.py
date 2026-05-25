import tensorflow as tf
import numpy as np
from PIL import Image
import os
from django.conf import settings

# Load model from the 'models' folder in your directory
MODEL_PATH = os.path.join(settings.BASE_DIR, 'models', 'skin_disease_model.h5')
# 2. Load the model globally once when the server boots up
print("Loading Keras Model...")
model = tf.keras.models.load_model(MODEL_PATH)
print("Model loaded successfully.")

# HAM10000 exact label mapping
CLASSES = [
    'akiec', # Actinic keratoses
    'bcc',   # Basal cell carcinoma
    'bkl',   # Benign keratosis-like lesions
    'df',    # Dermatofibroma
    'mel',   # Melanoma
    'nv',    # Melanocytic nevi
    'vasc'   # Vascular lesions
]

def predict_skin_disease(image_path):
    """
    Accepts an image file path, preprocesses it, runs inference through 
    the H5 model, and returns the predicted label string.
    """
    # Load and preprocess
    img = Image.open(image_path).convert('RGB').resize((224, 224))
    img_array = np.array(img) / 255.0

    # Expand array dimensions to simulate a batch: shape becomes (1, 224, 224, 3)
    img_array = np.expand_dims(img_array, axis=0)
    
    predictions = model.predict(img_array)
    index = np.argmax(predictions)
    return CLASSES[index]