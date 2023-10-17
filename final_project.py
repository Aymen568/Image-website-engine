from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch.helpers import bulk
import pandas as pd

# Connect to Elasticsearch
es = Elasticsearch(hosts=['localhost'], port=9200)

# Define the index settings and mappings
index_name = 'index14'

settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "path": {
                "type": "keyword"
            },
            "features_dense1": {
                "type": "dense_vector",
                "dims": 1024
            },
            "features_dense2": {
                "type": "dense_vector",
                "dims": 517
            },
            "features_dense3": {
                "type": "dense_vector",
                "dims": 517
            }
        }
    }
}

# Create the index
es.indices.create(index=index_name, body=settings)

# Read data from CSV file
data = pd.read_csv('C:\\Users\\aymen\\Desktop\\tp1-indexation\\tp1\\feature_vectors.csv')

# Prepare the data for bulk indexing
bulk_data = []
for _, row in data.iterrows():
    doc = {
        "_index": index_name,
        "_source": {
            "path": row['path'],
            "features_dense1": row.iloc[1:1025].values.tolist(),
            "features_dense2": row.iloc[1025:1542].values.tolist(),
            "features_dense3": row.iloc[1542:].values.tolist()
        }
    }
    bulk_data.append(doc)

# Perform bulk indexing
helpers.bulk(es, bulk_data)

