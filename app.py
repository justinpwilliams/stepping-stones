from flask import Flask, request, jsonify, render_template

import graph

app = Flask(__name__)


@app.route("/")
def index():
    print("Home page requested")
    return render_template("index.html")


@app.route("/ac_test", methods=["POST", "GET"])
def ac_test():
    print("Concept selection page requested")
    if request.method == "GET":
        concepts = graph.load_topics('LectureBank-master/LB-Paper/208topics.csv')
        concepts = list(concepts['Name'])

        return render_template("ac_test.html", concepts=concepts)


if __name__ == '__main__':
    app.run()
