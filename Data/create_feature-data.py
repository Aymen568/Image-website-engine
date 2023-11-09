# inceptionv3_feature_extraction.py
from tensorflow import keras
from keras.models import Model
from keras.applications.inception_v3 import InceptionV3, preprocess_input
from sklearn.metrics.pairwise import cosine_similarity
from skimage.feature import local_binary_pattern
import numpy as np
import cv2
import os
import pandas as pd

# Load pre-trained InceptionV3 model
base_model = InceptionV3(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.layers[-2].output)  # Remove the final softmax layer

# Preprocess input image and extract features
def extract_inceptionv3_features(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (299, 299))  # InceptionV3 input size
    img = preprocess_input(img)
    img = np.expand_dims(img, axis=0)
    features = model.predict(img)
    return features
def extract_lbp_features(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    radius = 1
    n_points = 8 * radius
    lbp_image = local_binary_pattern(img, n_points, radius, method='uniform')
    hist, _ = np.histogram(lbp_image.ravel(), bins=np.arange(0, n_points + 3), range=(0, n_points + 2))
    hist = hist.astype("float")
    hist /= (hist.sum() + 1e-7)  # Normalize the histogram
    return hist

def get_image_files(root_dir):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
    image_files = []

    for category in os.listdir(root_dir):
        category_path = os.path.join(root_dir, category)
        if os.path.isdir(category_path):
            for root, _, files in os.walk(category_path):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in image_extensions):
                        image_files.append(os.path.join(root, file))

    return image_files

# Combine InceptionV3 and LBP features
def combine_features(inceptionv3_features, lbp_features):
    return np.concatenate((inceptionv3_features, lbp_features), axis=None)
def compute_euclidean_distance(query_vector, dataset_vectors):
    # Compute the Euclidean distance between the query vector and each dataset vector
    distances = np.linalg.norm(dataset_vectors - query_vector, axis=1)
    return distances


root_directory = r"C:\Users\aymen\Desktop\tp1-indexation\tp1\bdimage\idb"
image_files = get_image_files(root_directory)


final_vector_list=[]

for image_path in image_files:
    googlenet_features=extract_inceptionv3_features(image_path)
    lbp_features=extract_lbp_features(image_path)
    final_vector=combine_features(googlenet_features, lbp_features)
    final_vector_list.append(final_vector)


feature_vector_df = pd.DataFrame(final_vector_list)
feature_vector_df.to_csv("feature_vectors.csv", index=False)
paths_df = pd.DataFrame(image_files)

paths_df.to_csv("paths.csv", index=False)

# Concatenate the two DataFrames
combined_df = pd.concat([paths_df, feature_vector_df], axis=1)

# Save the combined DataFrame to a CSV file
combined_df.to_csv("Final_Data.csv", index=False)
