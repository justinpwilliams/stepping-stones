import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

topics_file = "LectureBank-master/LB-Paper/208topics.csv"
prereq_file = "LectureBank-master/LB-Paper/prerequisite_annotation.csv"


def load_topics(filename=topics_file):
    return pd.read_csv(filename, names=['ID', 'Name', 'Link'])


def load_prereqs(filename=prereq_file):
    return pd.read_csv(filename)


def make_graph(topics, prereqs):
    g = nx.DiGraph()

    # Add Nodes
    g.add_nodes_from([(topic[0], {"name": topic[1], "link": topic[2]}) for topic in topics.values])

    # Add directed edges when prerequisite relationship is true
    g.add_edges_from([(ids[0], ids[1]) for ids in prereqs.values if ids[2] == 1])
    return g