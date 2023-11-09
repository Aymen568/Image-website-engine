from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
import cv2
from io import BytesIO
from tensorflow import keras
from keras.models import Model
from keras.applications.inception_v3 import InceptionV3, preprocess_input
from skimage.feature import local_binary_pattern

# Load pre-trained InceptionV3 model
base_model = InceptionV3(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.layers[-2].output)  # Remove the final softmax layer

# Preprocess input image and extract features
def extract_inceptionv3_features(img):
    img = cv2.resize(img, (299, 299))  # InceptionV3 input size
    img = preprocess_input(img)
    img = np.expand_dims(img, axis=0)
    features = model.predict(img)
    return features

def extract_lbp_features(img):
    if len(img.shape) == 3 and img.shape[2] == 3:
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        img_gray = img
    radius = 1
    n_points = 8 * radius
    lbp_image = local_binary_pattern(img_gray, n_points, radius, method='uniform')
    hist, _ = np.histogram(lbp_image.ravel(), bins=np.arange(0, n_points + 3), range=(0, n_points + 2))
    hist = hist.astype("float")
    hist /= (hist.sum() + 1e-7)  # Normalize the histogram
    return hist

# Combine InceptionV3 and LBP features
def combine_features(inceptionv3_features, lbp_features):
    return np.concatenate((inceptionv3_features, lbp_features), axis=None)

app = Flask(__name__)

@app.route('/extract_features', methods=['POST'])
def extract_features():
    try:
        print(0)
        # Get the uploaded image from the request
        image_file = request.files['image']
        print(image_file)
        
        if not image_file:
            print("no image file")
            return jsonify({'error': 'No image provided'}), 400
        # Process the image and extract features
        print(1)
        image = Image.open(image_file)
        print(2)
        img_array = np.array(image)
        print(3)
        inceptionv3_features = extract_inceptionv3_features(img_array)
        lbp_features = extract_lbp_features(img_array)
        combined_features = combine_features(inceptionv3_features, lbp_features)
        print(4)
        # Return the combined features as a JSON response
        return jsonify({'features': combined_features.tolist()}), 200

    except Exception as e:
        print(5)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)