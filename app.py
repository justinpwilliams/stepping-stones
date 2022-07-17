from flask import Flask, request, jsonify, render_template

import graph

topics_file = "data/208topics.csv"
prereq_file = "data/prerequisite_annotation.csv"
taxonomy_file = "data/taxonomy.tsv"
concepts = graph.load_topics(topics_file)
prereqs = graph.load_prereqs(prereq_file)
concept_graph = graph.make_graph(concepts, prereqs)
taxonomy = graph.read_taxonomy(taxonomy_file)

goal_ids = []
mastered_ids = []

app = Flask(__name__)


@app.route("/")
def index():
    print("Home page requested")
    return render_template("index.html")


@app.route("/ac_test", methods=["POST", "GET"])
def ac_test():
    global concepts
    global goal_ids
    global mastered_ids
    print("Concept selection page requested")
    if request.method == "GET":
        concepts = list(concepts['Name'])
        return render_template("ac_test.html", concepts=concepts)


@app.route("/goal_concept", methods=['POST'])
def get_goal_concepts():
    global goal_ids
    if request.method == "POST":
        goal_concepts = request.form.get("goal_concepts", '')
        print(f'{goal_concepts} concepts received')
        goal_ids = graph.get_concept_ids_from_names(goal_concepts)

    return goal_concepts


@app.route("/mastered_concepts", methods=['POST'])
def get_mastered_concepts():
    global mastered_ids
    if request.method == "POST":
        mastered_concepts = request.form.get("mastered_concepts", '')
        print(f'{mastered_concepts} concepts received')
        mastered_ids = graph.get_concept_ids_from_names(mastered_concepts)
        print(f'{mastered_ids} are their ids.')

    return mastered_concepts


@app.route("/show_graph")
def show_graph():
    print("Call to show_graph")
    graph.get_graph_json(concept_graph, goal_ids, mastered_ids)
    return render_template("force.html")


if __name__ == '__main__':
    app.run()
