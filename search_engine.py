from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import os
import matplotlib.pyplot as plt
import numpy as np
from autocorrect import Speller
import io
import imghdr

spell = Speller(lang ="en")
index_name = 'index2'
def search_by_image_query(feature_vector=None, number = 0):
    if feature_vector is None:
        raise ValueError("Please enter an Image ID or a Feature Vector")
    query = {
                "query": {
                    "elastiknn_nearest_neighbors": {
                        "vec": feature_vector,
                        "field": "vector",
                        "similarity": "cosine",
                        "model": "lsh",
                        "candidates": 3
                    }
                }
            }
    res = es.search(index=index_name, body=query, size=number)
    hits = res['hits']['hits']
    st.subheader("Search Results:")
    images_per_column = 3
    for i in range(0, len(hits), images_per_column):
        column = st.columns(images_per_column)
        for j in range(i, min(i + images_per_column, len(hits))):
            hit = hits[j]
            path = hit['_source']["path"]
            with column[j % images_per_column]:
                image = Image.open(path)
                st.image(image, caption="Image from Elasticsearch n*{}".format(j), use_column_width=True)

def is_valid_image_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        return True
    except Exception as e:
        return False
  
# Create Elasticsearch client
es = Elasticsearch("http://localhost:9200")
# Streamlit interface
st.set_page_config(
    page_title="Image Web Search",
    page_icon="media\Search Engine.png",
    layout="wide"  # Use a wide layout to control the placement of the elements
)
col1,col2 = st.columns([1,5])
# App Logo (top left of the left column)
app_logo = Image.open("media\Search Engine.png")  # Replace with your app's logo
col1.image(app_logo, use_column_width=False, width=150)
col2.markdown("<h1 style='color: red; text-align: left;'>Image Web Search</h1>", unsafe_allow_html=True)


def main_page():
    option = st.sidebar.selectbox("Search by", ["Tag", "Similarity"])
    if option == "Tag":
        tags_input = st.sidebar.text_input("Enter Tags (comma-separated)", "")
        num_results = st.sidebar.slider("Select the number of pictures to display", min_value=1, max_value=20, value=4)
        if st.button("Search") or tags_input:
            # Split the input tags by commas and trim spaces
            tags = [tag.strip() for tag in tags_input.split(",")]
            # Number of pictures to display
            tags = [spell(tag) for tag in tags]
            # Define the search query based on the entered tags
            search_body = {
                "size": num_results,  # Adjust the size as needed
                "query": {
                    "terms": {
                        "tags": tags
                    }
                }
            }

            # Specify the index to search (in this case, 'flickrphotos')
            index_name = 'flickrphotos'

            # Perform the search
            try:
                response = es.search(index=index_name, body=search_body)
                hits = response['hits']['hits']
                # Display search results with columns
                st.subheader("Search Results:")

                # Specify the number of images per column
                images_per_column = 3

                for i in range(0, len(hits), images_per_column):
                    column = st.columns(images_per_column)
                    for j in range(i, min(i + images_per_column, len(hits))):
                        hit = hits[j]
                        source = hit['_source']
                        with column[j % images_per_column]:
                            st.write(f"Title: {source.get('title', 'N/A')}")
                            #st.write(f"Tags: {source.get('tags', 'N/A')}")
                            farm = source.get('flickr_farm', 'N/A')
                            server = source.get('flickr_server', 'N/A')
                            photo_id = source.get('id', 'N/A')
                            secret = source.get('flickr_secret', 'N/A')
                            image_url = f"http://farm{farm}.staticflickr.com/{server}/{photo_id}_{secret}.jpg"
                            if is_valid_image_url(image_url):
                                st.image(image_url, caption=f"Image for {source.get('title', 'N/A')}")
                            else:
                                continue
                st.write(f"Total hits: {len(hits)}")

            except Exception as e:
                st.error(f"Error: {e}")

    elif option == "Similarity":
        image2 = None
        st.sidebar.write("Choose an action:")
        action = st.sidebar.radio("Action", ("Load URL", "Upload Image"))
        if action == "Load URL":
            image_url = st.sidebar.text_input("Enter Image URL")
            if (image_url):
                try:
                    print(0)
                    response = requests.get(image_url)
                    print(1)
                    image2 = Image.open(BytesIO(response.content))
                except Exception as e:
                    print(2)
                    st.write(f"Error: {e}")
        else:
            uploaded_image = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
            if uploaded_image is not None:
                print("upload successful")
                image2 = Image.open(uploaded_image)
                print("open successful")
        print(3)
        num_pictures = st.sidebar.slider("Select the number of pictures to display", min_value=1, max_value=20, value=5)
        if (image2 is not None):
            st.image(image2, caption="Input Image", use_column_width=True)
            image_bytes = io.BytesIO()
            image2.save(image_bytes, format="JPEG")  # Save as JPEG (You can change the format as needed)
            image_bytes.seek(0)  # Reset the stream position
            image_format = imghdr.what(None, h=image_bytes.read())
            if image_format is None:
                image_format = "jpeg"
            # Map the detected image format to the appropriate content type
            content_type = {
                "jpeg": "image/jpeg",
                "jpg": "image/jpeg",
                "png": "image/png",
            }.get(image_format, "image/jpeg")  # Default to JPEG if format is unknown

            # Convert the image bytes to a numpy array
            image_data = np.array(image_bytes.getvalue())
            files = {'image': ("image." + image_format, image_data, content_type)}
            response = requests.post("http://127.0.0.1:5000/extract_features", files=files)
            if response.status_code == 200:
                features = response.json()['features']
                search_by_image_query(feature_vector = features, number= num_pictures)
            else:
                st.write("Error extracting features. Check your API.")
            # Display images on the right sidebar
main_page()
st.markdown("---")
st.markdown("<p style='color: black;'>© 2023 Image Web Search. All rights reserved.</p>", unsafe_allow_html=True)
st.markdown("<p style='color: black;'>Contributors: [BEN SALEM Ahmed], [LABIDI Aymen]</p>", unsafe_allow_html=True)
st.markdown("[GitHub Repository](https://github.com/your-repo)", unsafe_allow_html=True)
        
