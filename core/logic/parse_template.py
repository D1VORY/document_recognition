import json
import re

import Levenshtein as lev
import numpy as np

from core.logic.graph import DocumentGraph, Node


class JSONTemplate:
    def __init__(self, data: dict):
        self.languages = data.get('language')
        self.fields = data.get('fields')
        self.graph = DocumentGraph()
        self.correspondance_dict = {}  # key - id in photo; value - id in template;

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

    def get_corresponding_template_node(self, image_node):
        node_id = self.correspondance_dict.get(image_node.id)
        if not node_id:
            raise ValueError('Node does not have a corrseponding item')
        return self.graph.get_node_by_id(node_id)

    @staticmethod
    def _clear_string(string):
        return string.replace('/n', '').replace('/r', '').strip()

    @classmethod
    def get_distance(cls, a: str, b: str):
        a = cls._clear_string(a)
        b = cls._clear_string(b)
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
                self.correspondance_dict[closest_candidate.id] = anchors[i].id
        return target_anchors

    def _extract_values(self, image_anchors, image_nodes):
        image_values = []
        for image_anchor in image_anchors:
            corr_json_anchor = self.get_corresponding_template_node(image_anchor)
            image_anchor_relations = image_anchor.get_existing_relations()
            json_anchor_relations = corr_json_anchor.get_existing_relations()
            for json_position, json_node in json_anchor_relations.items():
                corresponding_image_node = image_anchor.get_corresponding_attr(json_position)
                regexp = json_node.value
                matches = re.match(regexp, corresponding_image_node.value)
                if matches:
                    image_values.append(corresponding_image_node)
                    self.correspondance_dict[corresponding_image_node.id] = json_node.id
        return image_values

    def build_dict_response(self, values):
        res = {}
        for val in values:
            corrseponding_json_node = self.graph.get_node_by_id(self.correspondance_dict.get(val.id))
            if corrseponding_json_node:
                res[corrseponding_json_node.name] = val.value
        return res

    def compare(self, graph):
        """Compares template graph with graph from photo, returns corresponding nodes"""
        image_nodes = graph.nodes
        extracted_anchors = self._extract_anchors(image_nodes)
        values = self._extract_values(extracted_anchors, image_nodes)
        response = self.build_dict_response(values)
        return response
