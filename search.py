import requests
import utils
import os
from elasticsearch import Elasticsearch

#res = requests.get("http://localhost:9200/_features")
#print(res.text)

ES_HOST = "http://127.0.0.1:9200" #security is disabled for testing purposes
elastic_search = Elasticsearch(ES_HOST)

#print(elastic_search.indices.get(index='nice_index'))

