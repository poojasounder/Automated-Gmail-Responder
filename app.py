"""
A simple retrieval-augmented generation LLM app.
"""
import flask
import os
from llm import myllm
from query import Query

app = flask.Flask(__name__)       # our Flask app

app.secret_key = os.urandom(24)

app.add_url_rule('/',
                 view_func=Query.as_view('query'),
                 methods=["GET", 'POST'])

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))
