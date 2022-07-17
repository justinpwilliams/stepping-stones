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
        concepts = graph.load_topics('../LectureBank-master/LB-Paper/208topics.csv')
        concepts = list(concepts['Name'])
    return render_template("ac_test.html", concepts=concepts)


@app.route("/goal_concept", methods=['POST'])
def get_goal_concepts():
    if request.method == "POST":
        goal_concepts = request.form.get("goal_concepts", '')
        print(f'{goal_concepts} concepts received')

    return goal_concepts


@app.route("/mastered_concepts", methods=['POST'])
def get_mastered_concepts():
    if request.method == "POST":
        mastered_concepts = request.form.get("mastered_concepts", '')
        print(f'{mastered_concepts} concepts received')

    return mastered_concepts


if __name__ == '__main__':
    app.run()
