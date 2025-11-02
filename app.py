from flask import Flask, render_template, request, redirect, url_for
import search
import utils

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/match_all")
def match_all():

    results = []

    query_todo = {"query": {"match_all": {}}, "size" : 1000}

    query_result = utils.query(query_todo)

    results = [
        {
            "title": hit["_source"]["title"],
            "content": hit["_source"]["content"],
            "score": hit["_score"]
        }
        for hit in query_result["hits"]["hits"]
    ]

    return render_template("match_all.html", results=results)


@app.route("/match", methods=["GET", "POST"])
def match():

    results = []
    query_term = ""
    field = "content" #by default, we search in content

    if request.method == "POST":

        query_term = request.form.get("query_term", "")
        field = request.form.get("field", "content")

        query_todo = {"query": 
                        {"match": 
                            {field: query_term}
                            },
                        "size" : 1000
                    }
        
        query_result = utils.query(query_todo)

        results = [
            {
                "title": hit["_source"]["title"],
                "content": hit["_source"]["content"],
                "score": hit["_score"]
            }
            for hit in query_result["hits"]["hits"]
        ]

    return render_template("match.html", results=results, query=query_term, field=field)


@app.route("/multi", methods=["GET", "POST"])
def multi():

    results = []
    query_term = ""

    if request.method == "POST":

        query_term = request.form.get("query_term", "")
        query_todo = {
            "query": {
                "multi_match": {
                    "query": query_term,
                    "fields": ["title", "content"]
                }
            },
            "size" : 1000
        }

        query_result = utils.query(query_todo)

        results = [
            {
                "title": hit["_source"].get("title", "Untitled"),
                "content": hit["_source"].get("content", ""),
                "score": hit["_score"]
            }
            for hit in query_result["hits"]["hits"]
        ]
        
    return render_template("multi.html", results=results, query=query_term)


@app.route("/phrase", methods=["GET", "POST"])
def phrase():

    results = []
    query_term = ""

    if request.method == "POST":

        query_term = request.form.get("query_term", "")
        query_todo = {"query": 
                        {"match_phrase": 
                            {"content": query_term}
                            },
                        "size" : 1000
                        }
        
        query_result = utils.query(query_todo)

        results = [
            {
                "title": hit["_source"].get("title", "Untitled"),
                "content": hit["_source"].get("content", ""),
                "score": hit["_score"]
            }
            for hit in query_result["hits"]["hits"]
        ]

    return render_template("phrase.html", results=results, query=query_term)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=6749, debug=True)

