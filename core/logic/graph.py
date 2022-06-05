import itertools
import Levenshtein as lev
import numpy as np


class Node:
    newid = itertools.count()

    class NodePosition:
        TOP = 'TOP'
        BOTTOM = 'BOTTOM'
        RIGHT = 'RIGHT'
        LEFT = 'LEFT'
        TOP_RIGHT = 'TOP_RIGHT'
        TOP_LEFT = 'TOP_LEFT'
        BOTTOM_RIGHT = 'BOTTOM_RIGHT'
        BOTTOM_LEFT = 'BOTTOM_LEFT'

    class NodeType:
        ANCHOR = 'anchor'
        VALUE = 'value'
        DEFAULT = 'default'

    def __init__(self, value='', name='unkown', node_type=NodeType.DEFAULT, node_id: int=None):
        self.value = value
        self.name = name
        self.node_type = node_type
        self.id = node_id or next(self.newid)

        self.right_node = None
        self.left_node = None
        self.top_node = None
        self.bottom_node = None
        self.top_right_node = None
        self.top_left_node = None
        self.bottom_right_node = None
        self.bottom_left_node = None

    @classmethod
    def get_reversed_position(cls, position):
        reversed = {
            cls.NodePosition.TOP: cls.NodePosition.BOTTOM,
            cls.NodePosition.BOTTOM: cls.NodePosition.TOP,
            cls.NodePosition.RIGHT: cls.NodePosition.LEFT,
            cls.NodePosition.LEFT: cls.NodePosition.RIGHT,
            cls.NodePosition.TOP_RIGHT: cls.NodePosition.BOTTOM_LEFT,
            cls.NodePosition.TOP_LEFT: cls.NodePosition.BOTTOM_RIGHT,
            cls.NodePosition.BOTTOM_LEFT: cls.NodePosition.TOP_RIGHT,
            cls.NodePosition.BOTTOM_RIGHT: cls.NodePosition.TOP_LEFT,
        }
        return reversed.get(position)


    def get_corresponding_attr(self, position: str):
        if position == self.NodePosition.RIGHT:
            return self.right_node
        elif position == self.NodePosition.TOP_RIGHT:
            return self.top_right_node
        elif position == self.NodePosition.TOP:
            return self.top_node
        elif position == self.NodePosition.TOP_LEFT:
            return self.top_left_node
        elif position == self.NodePosition.LEFT:
            return self.left_node
        elif position == self.NodePosition.BOTTOM_LEFT:
            return self.bottom_left_node
        elif position == self.NodePosition.BOTTOM:
            return self.bottom_node
        elif position == self.NodePosition.BOTTOM_RIGHT:
            return self.bottom_right_node

    def set_to_corresponding_attr(self, position: str, node):
        if position == self.NodePosition.RIGHT:
            self.right_node = node
        elif position == self.NodePosition.TOP_RIGHT:
            self.top_right_node = node
        elif position == self.NodePosition.TOP:
            self.top_node = node
        elif position == self.NodePosition.TOP_LEFT:
            self.top_left_node = node
        elif position == self.NodePosition.LEFT:
            self.left_node = node
        elif position == self.NodePosition.BOTTOM_LEFT:
            self.bottom_left_node = node
        elif position == self.NodePosition.BOTTOM:
            self.bottom_node = node
        elif position == self.NodePosition.BOTTOM_RIGHT:
            self.bottom_right_node = node
        return self.get_corresponding_attr(position)

    def set_relation(self, other_node, position):
        if not self.get_corresponding_attr(position):
            self.set_to_corresponding_attr(position, other_node)
            reversed_position = self.get_reversed_position(position)
            other_node.set_to_corresponding_attr(reversed_position, self)

    def __repr__(self):
        return f'{self.id} | {self.value}'


class DocumentGraph:
    def __init__(self, nodes=None):
        self.nodes = nodes or []
        self._nodes_ids = {node.id: index for index, node in zip(range(len(self.nodes)), self.nodes)}

    def add_to_graph(self, node: Node):
        if node.id in self._nodes_ids:
            raise ValueError('THIS ID ALREADY PRESENT')
        self.nodes.append(node)
        self._nodes_ids[node.id] = len(self.nodes) - 1

    def remove_from_graph(self, node: Node):
        pass

    def get_node_by_id(self, id:int)->Node:
        index = self._nodes_ids.get(id)
        if index is None:
            return None
        return self.nodes[index]


class PhotoDocumentGraph(DocumentGraph):
    def extract_features(self, nodes):
        pass


class TemplateDocumentGraph(DocumentGraph):
    @staticmethod
    def get_distance(a: str, b: str):
        dist = lev.distance(a, b)
        return dist / max(len(a), len(b))

    def _get_anchors(self):
        return [node for node in self.nodes if node.node_type == Node.NodeType.ANCHOR]

    def _extract_anchors(self, nodes, thresh=0.5):
        anchors = self._get_anchors()
        anchors_len = len(anchors)
        nodes_len = len(nodes)
        distance_matrix = np.zeros(shape=(anchors_len, nodes_len))
        for i in range(anchors_len):
            for j in range(nodes_len):
                distance = self.get_distance(anchors[i].value, nodes[j].value)
                if distance > thresh:
                    distance=1.0
                distance_matrix[i, j] = distance
        indeces_of_sorted = np.argsort(distance_matrix, axis=1)
        for i in range(anchors_len):
            pass
        return 'cum'

    def compare(self, graph):
        """Compares template graph with graph from photo, returns corresponding nodes"""
        self._extract_anchors(graph.nodes)

