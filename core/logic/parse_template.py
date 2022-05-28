import json

from core.logic.graph import DocumentGraph, Node


class JSONTemplate:
    def __init__(self, data: dict):
        self.languages = data.get('language')
        self.fields = data.get('fields')
        self.graph = DocumentGraph()

    def build_graph(self):
        for field in self.fields:
            node = Node(
                node_id=field.get('id'),
                node_type=field.get('type'),
                name=field.get('name'),
            )
            self.graph.add_to_graph(node)
        for field, node in zip(self.fields, self.graph.nodes):
            for position in field.get('position', []):
                position_direction = position.get('pos')
                other_node = self.graph.get_node_by_id(position.get('dep_id'))
                node.set_relation(other_node, position_direction)



dct = json.load(open('v3.json'))
tplt = JSONTemplate(dct)
tplt.build_graph()

print('IM FUCKING UMMING')
