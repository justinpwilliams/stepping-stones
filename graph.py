import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

topics_file = "data/208topics.csv"
prereq_file = "data/prerequisite_annotation.csv"
lecture_file = "data/lecturebank.tsv"


def load_topics(filename=topics_file):
    return pd.read_csv(filename, names=['ID', 'Name', 'Link'])


def load_prereqs(filename=prereq_file):
    return pd.read_csv(filename)


def make_graph(topics, prereqs):
    g = nx.DiGraph()

    # Add Nodes
    # g.add_nodes_from([(topic[0], {"name": topic[1], "link": topic[2]}) for topic in topics.values])
    g.add_nodes_from([(topic[0], {"name": topic[1]}) for topic in topics.values])

    # Add directed edges when prerequisite relationship is true
    g.add_edges_from([(ids[0], ids[1]) for ids in prereqs.values if ids[2] == 1])
    return g


def load_lectures(lecture_file=lecture_file):
    return pd.read_csv(lecture_file, names=["ID", "Title", "URL", "Topic_ID", "Year", "Instructor", "Path", "Venue"],
                       sep="\t")


def read_taxonomy(taxonomy_file):
    return pd.read_csv(taxonomy_file, sep="\t")


def get_lookup_topic(concept_name: str, taxonomy: pd.DataFrame) -> int:
    matches = taxonomy['topic_name'].str.contains(concept_name.lower(), case=False, regex=False)
    if matches is None:
        pass  # TODO add lecture lookup.
    return taxonomy[matches]['true_id'].values


def generate_subgraph(concept_graph, goal_concept_id, mastered_concept_id: list = []):
    """
    Generate a concept tree from the concept graph_to_draw given one or more goal concepts and one or more mastered concepts.
    :param concept_graph: The graph_to_draw of concepts which should contain the goal_concepts and mastered_concepts
    :param goal_concepts: Iterable of Goal concept ids
    :param mastered_concepts: Iterable of mastered concept ids
    :return: The graph_to_draw of mastered concepts with paths to goal concepts.
    """
    # # BFS from goal
    # subgraph = nx.bfs_tree(concept_graph, source=goal_concept_id, reverse=True)

    # Find ancestors from Goal
    # TODO make work for multiple goals
    for goal in goal_concept_id:
        goal_ancestors = set(nx.ancestors(concept_graph, goal))
        goal_ancestors.add(goal)

    mastered_ancestors = set()

    # Find mastered and ancestors of mastered
    for mastered_concept in mastered_concept_id:
        # if mastered_concept_id:
        mastered_ancestors.update(nx.ancestors(concept_graph, mastered_concept))
        # mastered_ancestors.add(mastered_concept)  # Keep mastered

    # Remove mastered and ancestors of mastered from goal and ancestors
    goal_ancestors = list(goal_ancestors - mastered_ancestors)

    # return subgraph of goal and ancestors minus all mastered and ancestors.
    return concept_graph.subgraph(goal_ancestors)


def draw_graph(graph_to_draw):
    nx.draw(graph_to_draw, arrows=True, with_labels=True)
    plt.show()


def get_concept_id_from_name(name: str) -> int:
    print(f"Looking for {name}")
    topics = load_topics()
    return int(topics[topics.Name == name]['ID'].values)


def get_concept_ids_from_names(names: str) -> list[int]:
    concept_list = names.replace('"','').split(',')
    concept_list.pop()  # Remove empty last string
    concept_list = [v.strip() for v in concept_list]
    print(f"Concept list searching for {concept_list}")
    concept_ids_captured = []
    for name in concept_list:
        concept_ids_captured.append(get_concept_id_from_name(name))
    return concept_ids_captured


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def get_graph_json(concept_graph, goal_concept_id, mastered_concept_id: list = []):
    """Returns graph in JSON format"""
    g = generate_subgraph(concept_graph, goal_concept_id, mastered_concept_id)
    j_format = nx.json_graph.node_link_data(g)
    json.dump(j_format, open("static/js/force.json", "w"), cls=NpEncoder)


if __name__ == "__main__":
    topics_file = "data/208topics.csv"
    prereq_file = "data/prerequisite_annotation.csv"
    taxonomy_file = "data/taxonomy.tsv"
    topics = load_topics(topics_file)
    prereqs = load_prereqs(prereq_file)
    graph = make_graph(topics, prereqs)
    taxonomy = read_taxonomy(taxonomy_file)

    # # Example 1: Goal Concept-Attention Models, No Mastered Concepts
    # # ex1_graph = generate_subgraph(graph, 12)
    # # draw_graph(ex1_graph)
    #
    # # Example 2: Goal Concept-Attention Models, One Mastered Concept
    # ex2_graph = generate_subgraph(graph, 12, [173])
    # draw_graph(ex2_graph)
    #
    # # Example 3: Goal Concept with one prerequisite
    # ex3_graph = generate_subgraph(graph, 155)
    # draw_graph(ex3_graph)
    #
    # # Example 4: 155 is a prereq of 24 and 47, how is this displayed.
    # ex4_graph = generate_subgraph(graph, 24)
    # draw_graph(ex4_graph)
    #
    # # Example 5: Should remove 47 and 155, doesn't TODO
    # ex5_graph = generate_subgraph(graph, 24, [47])
    # draw_graph(ex5_graph)

    # # Trying Concept from name
    concept = "Q Learning"
    concept_id = get_concept_id_from_name(concept)
    print(concept_id)
    concepts = "Q Learning, Markov decision processes, "
    concept_ids = get_concept_ids_from_names(concepts)
    print(concept_ids)

    # Trying JSON
    get_graph_json(graph, 24, [47])
