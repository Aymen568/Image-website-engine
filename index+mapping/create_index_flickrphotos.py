<<<<<<< HEAD
import json
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch.helpers import bulk
import pandas as pd

es = Elasticsearch(
    [ {'host': 'localhost', 'port': 9200, "scheme": "http"}],
    
)

# Define the index settings and mappings
index_name = 'flickrphotos'  # Replace with your desired index name
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name, ignore=[400, 404])

settings = {
    "number_of_shards": 1,
    "number_of_replicas": 0
}

mapping = {
    "properties": {
        "id": {"type": "text", "index": True},
        "userid": {"type": "text", "index": True},
        "title": {"type": "text", "index": True},
        "tags": {"type": "text", "index": True},
        "latitude": {"type": "double"},
        "longitude": {"type": "double"},
        "views": {"type": "integer"},
        "date_taken": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"},
        "date_uploaded": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"},
        "accuracy": {"type": "short"},
        "flickr_secret": {"type": "keyword", "index": True},
        "flickr_server": {"type": "keyword", "index": True},
        "flickr_farm": {"type": "keyword", "index": True},
        "x": {"type": "double"},
        "y": {"type": "double"},
        "z": {"type": "double"},
        "location": {"type": "geo_point"},
    }
}

# Create the index with settings and mappings
es.indices.create(index=index_name, body={"settings": settings, "mappings": mapping})

=======
import json
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch.helpers import bulk
import pandas as pd

es = Elasticsearch(
    [ {'host': 'localhost', 'port': 9200, "scheme": "http"}],
    
)

# Define the index settings and mappings
index_name = 'flickrphotos'  # Replace with your desired index name
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name, ignore=[400, 404])

settings = {
    "number_of_shards": 1,
    "number_of_replicas": 0
}

mapping = {
    "properties": {
        "id": {"type": "text", "index": True},
        "userid": {"type": "text", "index": True},
        "title": {"type": "text", "index": True},
        "tags": {"type": "text", "index": True},
        "latitude": {"type": "double"},
        "longitude": {"type": "double"},
        "views": {"type": "integer"},
        "date_taken": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"},
        "date_uploaded": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"},
        "accuracy": {"type": "short"},
        "flickr_secret": {"type": "keyword", "index": True},
        "flickr_server": {"type": "keyword", "index": True},
        "flickr_farm": {"type": "keyword", "index": True},
        "x": {"type": "double"},
        "y": {"type": "double"},
        "z": {"type": "double"},
        "location": {"type": "geo_point"},
    }
}

# Create the index with settings and mappings
es.indices.create(index=index_name, body={"settings": settings, "mappings": mapping})

>>>>>>> cc4bb1ac9d75efdad641106fd3514de1071cd2bb
