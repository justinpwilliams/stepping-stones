import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

topics_file = "LectureBank-master/LB-Paper/208topics.csv"
prereq_file = "LectureBank-master/LB-Paper/prerequisite_annotation.csv"
lecture_file = "LectureBank-master/LB-Paper/lecturebank.tsv"


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


def load_lectures(lecture_file=lecture_file):
    return pd.read_csv(lecture_file, names=["ID", "Title", "URL", "Topic_ID", "Year", "Instructor", "Path", "Venue"],
                       sep="\t")


if __name__ == "__main__":
    topics_file = "LectureBank-master/LB-Paper/208topics.csv"
    prereq_file = "LectureBank-master/LB-Paper/prerequisite_annotation.csv"
    topics = load_topics(topics_file)
    prereqs = load_prereqs(prereq_file)
    graph = make_graph(topics, prereqs)


def read_taxonomy(taxonomy_file):
    return pd.read_csv(taxonomy_file, sep="\t")


def get_lookup_topic(concept_name:str, taxonomy:pd.DataFrame)->int:
    matches = taxonomy['topic_name'].str.contains(concept_name.lower(), case=False, regex=False)
    if matches is None:
        pass  # TODO add lecture lookup.
    return taxonomy[matches]['true_id'].values