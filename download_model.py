import gdown
import os

MODEL_PATH = "models/skin_disease_model.h5"

if not os.path.exists(MODEL_PATH):
    os.makedirs("models", exist_ok=True)

    url = "https://drive.google.com/uc?id=19Hha8CAbHHHWxQV6X79fHytB6zYNc7AX"   

    gdown.download(url, MODEL_PATH, quiet=False)

print("Model ready!")