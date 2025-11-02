import os
from elasticsearch import Elasticsearch

ES_HOST = "http://127.0.0.1:9200" #security is disabled for testing purposes
es = Elasticsearch(ES_HOST)

def delete_index(index_name): #just in case
    res = es.indices.delete(index=index_name)
    print(res)

def txt_to_dict():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    files_path = os.path.join(script_dir, "files")
    files_data = []

    for filename in os.listdir(files_path):
        if filename.endswith(".txt"): #kinda useless as of now
            file_path = os.path.join(files_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            files_data.append({
                "title": os.path.splitext(filename)[0],  #filename without .txt
                "content": content
            })
    
    return files_data


def test_analyzer_content(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    files_path = os.path.join(script_dir, "files")
    file_path = os.path.join(files_path, f"{filename}.txt")
    with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

    return es.indices.analyze(index='nice_index', analyzer='content_analyzer', text=content)


def test_analyzer_title(filename):
    return es.indices.analyze(index='nice_index', analyzer='title_analyzer', text=filename)


def test_analyzer_content_all():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    files_path = os.path.join(script_dir, "files")

    for filename in os.listdir(files_path):
        print("\n")
        print("SEPARATORE SEXY")
        print("\n")
        print(test_analyzer_content(os.path.splitext(filename)[0]))


def test_analyzer_title_all():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    files_path = os.path.join(script_dir, "files")

    for filename in os.listdir(files_path):
        print("\n")
        print("SEPARATORE SEXY")
        print("\n")
        print(test_analyzer_title(filename))