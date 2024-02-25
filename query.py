from flask import redirect, request, url_for, render_template, session
from flask.views import MethodView
from llm import myllm

class Query(MethodView):
    def get(self):
        return render_template('query.html')

    def post(self):
        """
        Accepts POST requests, and processes the form;
        Redirect to index when completed.
        """
        answer = myllm.query(request.form['message'])
        return render_template('query.html',question=request.form['message'],answer=answer)
