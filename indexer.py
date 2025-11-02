#Indexes creator
import utils
import time
from elasticsearch import Elasticsearch

ES_HOST = "http://127.0.0.1:9200" #security is disabled for testing purposes
elastic_search = Elasticsearch(ES_HOST)

mapping = {
    'settings' : {
        'analysis':{
            'analyzer': {
                'title_analyzer' : {
                    'tokenizer' : 'underscore_tokenizer'    #we assume that titles are in the form name_number.txt
                },                                          #since this is a very small test use-case
                'content_analyzer' : {
                    'type' : 'standard',
                    'stopwords' : '_english_'               #might add emoji handling later
                }
            },
            'tokenizer': {
                'underscore_tokenizer': {
                'type': 'char_group',
                'tokenize_on_chars': [
                    "_"
                    ]
                } 
            },
        }
    },

    'mappings' : {
        'properties': {
            'title' : {'type':'text',
                        'analyzer': 'title_analyzer'},
            'content' : {'type':'text', 
                         'analyzer':'content_analyzer'}
        }
    }
}


#Delete index just in case
print(utils.delete_index('nice_index'))

#To measure time taken to create the index
start = time.time()

elastic_search.indices.create(index='nice_index', body=mapping)
docs = utils.txt_to_dict()
for doc in docs:
    elastic_search.index(index='nice_index', document=doc)

elapsed = time.time() - start
print(f"Ci ho messo {elapsed:.5f} secondi a indicizzare tutto, YIPPEEE")