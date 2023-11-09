import json
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch.helpers import bulk
import pandas as pd

es = Elasticsearch(
    [ {'host': 'localhost', 'port': 9200, "scheme": "http"}],
    
)

# Define the index settings and mappings
index_name = 'index3'  # Replace with your desired index name
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name, ignore=[400, 404])


settings = {
    "number_of_shards": 1,
    "number_of_replicas": 0,
}
mapping = {
    "dynamic": False,
    "properties": {
        "path": {"type": "text"},
        "vector": {
            "type": "elastiknn_dense_float_vector",
            "elastiknn": {
                "dims": 2058,
                "similarity": "l2",
                "model": "lsh",
                "L": 99,
                "k": 1,
                "w":3,
            }
        },
    }
}
# Create the index with settings and mappings
es.indices.create(index=index_name, body={"settings": settings, "mappings": mapping})

# Read data from CSV file
data = pd.read_csv('C:\\Users\\aymen\\Desktop\\tp1-indexation\\tp1\\Final_Data.csv')

# Prepare the data for bulk indexing

bulk_data = []

for _, row in data.iterrows():
    doc = {
        "_op_type": "index",
        "_index": index_name,
        "_source": {
            "path": row.iloc[0],
            "vector": row.iloc[1:].values.tolist(),
        }
    }
    bulk_data.append(doc)

batch_size = 1000  
batched_bulk_data = [bulk_data[i:i + batch_size] for i in range(0, len(bulk_data), batch_size)]

print("Indexing data in batches...")
for batch in batched_bulk_data:
    try:
        success, failed = helpers.bulk(es, batch, raise_on_error=False)
        for item in failed:
            print("\nERROR: Failed to index document:", item)
    except Exception as e:
        print("\nERROR:", e)
    
