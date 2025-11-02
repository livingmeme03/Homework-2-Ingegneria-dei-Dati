from flask import Flask, render_template, request
import search
import utils

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    query_term = ""
    field = "content"  #default search field

    if request.method == "POST":
        query_term = request.form.get("query_term", "")
        field = request.form.get("field", "content")

        if query_term:
            query_todo = {
                "query": {
                    "match": {
                        field: query_term
                    }
                }
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
    

    return render_template(
        'index.html', results=results, query=query_term, field=field
    )


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=6749, debug=True)

