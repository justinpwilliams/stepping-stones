import unittest
import matplotlib.pyplot as plt
import networkx as nx
import graph


class GraphTests(unittest.TestCase):
    def setUp(self) -> None:
        self.topics_file = "../LectureBank-master/LB-Paper/208topics.csv"
        self.prereq_file = "../LectureBank-master/LB-Paper/prerequisite_annotation.csv"
        self.prereq_file = "../LectureBank-master/LB-Paper/prerequisite_annotation.csv"
        self.taxonomy_file = "../LectureBank-master/LB-Paper/taxonomy.tsv"
        self.topics = graph.load_topics(self.topics_file)
        self.prereqs = graph.load_prereqs(self.prereq_file)
        self.taxonomy = graph.read_taxonomy(self.taxonomy_file)
        self.graph = graph.make_graph(self.topics, self.prereqs)

    def test_can_add_directed_edges_to_graph(self):
        self.assertTrue(16 in self.graph.successors(2))

    def test_can_draw_graph(self):
        nx.draw(self.graph, nodelist=list(self.graph.successors(2)),
                edgelist=[edge for edge in self.graph.edges if 2 in edge], with_labels=True)
        # plt.show()
        self.assertTrue(True)

    def test_can_find_shortest_path(self):
        path = nx.bidirectional_shortest_path(self.graph, 19, 59)
        print(path)
        self.assertLessEqual(len(path), 3)

    def test_can_find_simple_shortest_paths(self):
        simple_paths = list(nx.all_shortest_paths(self.graph, 154, 2))
        print(simple_paths)
        self.assertGreater(len(simple_paths), 0)

    def test_can_find_shortest_path_to_target(self):
        all_paths = nx.single_target_shortest_path(self.graph, 59)
        self.assertGreater(len(all_paths), 0)

    def test_can_load_lectures(self):
        lecture_file = '../LectureBank-master/LB-Paper/lecturebank.tsv'
        lectures = graph.load_lectures(lecture_file)

        # importing topic to list
        # Replace ID with topic name
        # lectures['Topic'] = self.topics['Name'][['Topic_ID'] == self.topics['ID']]
        self.assertIsNotNone(lectures)

    def test_can_reverse_graph(self):
        reversed = self.graph.reverse()
        print(list(reversed.predecessors(19)))
        self.assertTrue(2 in list(reversed.predecessors(19)))

    def test_find_arboresence_from_reversed(self):
        # reversed = self.graph_to_draw.reverse()
        # # preds = self.graph_to_draw.predecessors(152)
        # preds = nx.descendants(reversed, 152) # descendants of the reversed graph_to_draw.
        # print("Preds of 152, ", preds)
        # pred_sub = reversed.subgraph(set(preds).add(152)).copy()

        # BFS from goal
        # bfs_tree = nx.bfs_tree(self.graph_to_draw, source=12, reverse=True)
        # print(list(bfs_tree.edges()))
        # # bfs_tree.remove_nodes_from(nx.descendants(bfs_tree, 100)) # This method treats 109 as a terminal node
        # # print(list(bfs_tree.edges()))
        # nx.draw(bfs_tree, arrows=True, with_labels=True)
        # plt.show()

        subgraph = graph.generate_tree(self.graph, 12, 173)
        self.assertIsNotNone(subgraph)

    def test_can_read_taxonomy(self):
        self.assertIsNotNone(self.taxonomy)

    def test_can_match_topic_to_taxonomy_id(self):
        concept_name = "Topic modeling" # id 96 from 208 topics,
        topic_lookup_ids = graph.get_lookup_topic(concept_name, self.taxonomy)
        self.assertTrue(1179 in topic_lookup_ids)




if __name__ == '__main__':
    unittest.main()
