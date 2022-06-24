import unittest
import matplotlib.pyplot as plt
import networkx as nx
import graph


class GraphTests(unittest.TestCase):
    def setUp(self) -> None:
        self.topics_file = "../LectureBank-master/LB-Paper/208topics.csv"
        self.prereq_file = "../LectureBank-master/LB-Paper/prerequisite_annotation.csv"
        self.topics = graph.load_topics(self.topics_file)
        self.prereqs = graph.load_prereqs(self.prereq_file)
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


if __name__ == '__main__':
    unittest.main()
