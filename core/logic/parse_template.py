import json
import Levenshtein as lev
import numpy as np

from core.logic.graph import DocumentGraph, Node


class JSONTemplate:
    def __init__(self, data: dict):
        self.languages = data.get('language')
        self.fields = data.get('fields')
        self.graph = DocumentGraph()
        self.correspondance_dict = {}  # key - id in template; value - id in photo

    def build_graph(self):
        for field in self.fields:
            node = Node(
                node_id=field.get('id'),
                node_type=field.get('type'),
                name=field.get('name'),
                value=field.get('regex')
            )
            self.graph.add_to_graph(node)
        for field, node in zip(self.fields, self.graph.nodes):
            for position in field.get('position', []):
                position_direction = position.get('pos')
                other_node = self.graph.get_node_by_id(position.get('dep_id'))
                node.set_relation(other_node, position_direction)

    @staticmethod
    def get_distance(a: str, b: str):
        dist = lev.distance(a, b)
        return dist / max(len(a), len(b))

    def _get_anchors(self):
        return [node for node in self.graph.nodes if node.node_type == Node.NodeType.ANCHOR]

    def _extract_anchors(self, nodes, thresh=0.5):
        anchors = self._get_anchors()
        anchors_len = len(anchors)
        nodes_len = len(nodes)
        distance_matrix = np.zeros(shape=(anchors_len, nodes_len))
        for i in range(anchors_len):
            for j in range(nodes_len):
                distance = self.get_distance(anchors[i].value, nodes[j].value)
                if distance > thresh:
                    distance = 1.0
                distance_matrix[i, j] = distance
        indeces_of_sorted = np.argsort(distance_matrix, axis=1)

        target_anchors = []
        for i in range(anchors_len):
            closest_candidate_index = indeces_of_sorted[i, 0]
            closest_candidate_distance = distance_matrix[i, closest_candidate_index]
            closest_candidate = nodes[closest_candidate_index]
            if int(closest_candidate_distance) < 1:
                target_anchors.append(closest_candidate)
                self.correspondance_dict[anchors[i].id] = closest_candidate.id
        return target_anchors

    def _extract_values(self, anchors):
        pass

    def compare(self, graph):
        """Compares template graph with graph from photo, returns corresponding nodes"""
        target_nodes = graph.nodes
        extracted_anchors = self._extract_anchors(graph.nodes)
        values = self._extract_values()

# dct = json.load(open('v3.json'))
# tplt = JSONTemplate(dct)
# tplt.build_graph()
#
# print('IM FUCKING UMMING')
