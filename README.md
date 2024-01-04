
# <p align="center" style="font-size: 60px;"><strong>Content & Text Based Image Retrieval Search Engine</strong></p>
<p align="center" >
[Introduction](#introduction) |
[Functionalities](#functionalities) |
[Model Architecture](#model-architecture) |
[Results](#results) |
[Deployment](#deployment) |
[Tools](#tools) |
[Installation](#installation) |
[Topics](#topics)
</p>

  
## 🔗Introduction 
An image search engine that covers over 1 million annotated images from Open Images Dataset. Users can conveniently search using text, images, or a combination of both.
<div align="center">
  <img src="/media/Search%20Engine.png" alt="Logo" width="300" height="300">
</div>

## 🔗Functionnalities
This project employs Elasticsearch to store data and provides two primary functions:
1. Similarity Search: It retrieves the most similar images to a provided reference image.
2. Database search: It conducts searches based on image tags, enabling users to find images that match specific descriptors.
 
## 🔗Model Architecture
![Architecture](/media/transormation.png)

## 🔗Results
Below you can find some of the results:
![Architecture](/media/result1.png)

## 🔗 Deployment
Both the API and frontend of the web application are efficiently containerized using Docker and docker-compose. For more details, refer to the comprehensive report.

## 🔗Tools
- Frontend Development: Streamlit
- Backend Development: Flask
- Database: Elasticsearch 8.1.0 + Elasticknn plgin 8.1.0 (You can install it from this link: https://github.com/alexklibisz/elastiknn/releases/tag/8.1.0.0)
- Deployment: Docker
    
## 🔗Installation
In order to reproduce the project you have to:

    1- Clone the repository.
    2- Move to the project directory.
    3- Get the data index.
        * Unzip data fromthe folder data/photo_metadat.zip
        * Change paths in the file models/create_data.py and run it to create feature vectors 
        * Create a new index: execute the file create_index_flickrphotos.py
        * Execute the file mapping.py
    4- Run docker-compose up --build Once these steps are done, the web application should start in the browser.
    5- You can also execute the app.py.

## 🔗Topics:
    1- Backend Development, deployment
    2- Database Managment
    

