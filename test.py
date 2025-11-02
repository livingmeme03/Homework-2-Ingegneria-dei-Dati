import requests
import utils
import os
from elasticsearch import Elasticsearch

ES_HOST = "http://127.0.0.1:9200" #security is disabled for testing purposes
elastic_search = Elasticsearch(ES_HOST)

query1 = {
    "size" : 10,
    "query" : {
        "match_all" : {}
    }
}

query2 = {
    "query" : {
        "match" : {
            "title" : "1"
        }
    }
}


utils.print_query_results(query2)
#print(elastic_search.indices.get(index='nice_index'))