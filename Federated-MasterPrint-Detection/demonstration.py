import cv2
import numpy as np
import tensorflow as tf
import config  
import sys

# Suppress TensorFlow warnings
tf.get_logger().setLevel('ERROR')

# Loading the Trained Model
try:
    model = tf.keras.models.load_model("final_model.keras")
    print("--- Model 'final_model.keras' loaded successfully! ---")
except Exception as e:
    print(f"Error loading model: {e}")
    print("Please run 'py main_federated.py' first to train and save the model.")
    sys.exit()

# Defining the classes
CLASS_NAMES = ["GENUINE", "ATTACK (MasterPrint)"]

def predict_image(image_path):
    # Load and Preprocessing the Image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not read image at {image_path}")
        return

    # Resize to the 96x96 format the model was trained on
    img_resized = cv2.resize(img, (config.IMG_WIDTH, config.IMG_HEIGHT))
    
    # Add a "batch" dimension and normalize
    img_array = np.expand_dims(img_resized, axis=0)
    img_array = img_array.astype(np.float32) / 255.0

    # For Making Predictions
    predictions = model.predict(img_array, verbose=0)
    
    score = np.max(predictions[0])
    predicted_class_index = np.argmax(predictions[0])
    predicted_class_name = CLASS_NAMES[predicted_class_index]

    print("\n--- Prediction Result ---")
    print(f"Image: {image_path}")
    print(f"Prediction: ** {predicted_class_name} **")
    print(f"Confidence: {score * 100:.2f}%")

if __name__ == "__main__":
   
    if len(sys.argv) < 2:
        print("\n--- How to use this script ---")
        print("Drag and drop an image file onto this script, OR")
        print("Run in terminal: py demo.py [path_to_your_image]")
        print("\nExample: py demo.py data/FVC2004/db1_101_1.tif")
    else:
        predict_image(sys.argv[1])