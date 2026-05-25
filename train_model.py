import os
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from sklearn.model_selection import train_test_split

# # 1. SETUP PATHS (Adjust these to where you downloaded HAM10000)

# 1. SETUP PATHS
# Use raw strings (r'...') so Windows backslashes don't cause errors
data_dir = r'C:\Users\minte\Desktop\HAM_1000\HAM10000_images_part_1' 
metadata_path = r'C:\Users\minte\Desktop\HAM_1000\HAM10000_metadata.csv'

# data_dir = 'path/to/HAM10000_images' 
# metadata_path = 'path/to/HAM10000_metadata.csv'

# 2. LOAD METADATA
data = pd.read_csv(metadata_path)
# Mapping IDs to actual image paths
data['path'] = data['image_id'].map(lambda x: os.path.join(data_dir, f'{x}.jpg'))
# Encode labels (akiec, bcc, bkl, df, mel, nv, vasc)
data['label'] = pd.Categorical(data['dx']).codes

# 3. PREPROCESS & SPLIT
# We resize to 224x224 to match your Django utils.py
IMG_WIDTH, IMG_HEIGHT = 224, 224

train_df, test_df = train_test_split(data, test_size=0.2, random_state=42, stratify=data['dx'])

datagen = ImageDataGenerator(rescale=1./255)

train_loader = datagen.flow_from_dataframe(
    train_df, x_col='path', y_col='dx',
    target_size=(IMG_WIDTH, IMG_HEIGHT),
    batch_size=32, class_mode='categorical'
)

# 4. BUILD THE CNN MODEL
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(7, activation='softmax') # 7 classes in HAM10000
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# 5. TRAIN
print("Starting training...")
model.fit(train_loader, epochs=10) # Increase epochs for better accuracy

# 6. SAVE THE FILE
model.save('models/skin_disease_model.h5')
print("Model saved as skin_disease_model.h5")