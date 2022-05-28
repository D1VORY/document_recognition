import itertools


class Node:
    newid = itertools.count()
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
            cls.TOP: cls.BOTTOM,
            cls.BOTTOM: cls.TOP,
            cls.RIGHT: cls.LEFT,
            cls.LEFT: cls.RIGHT,
            cls.TOP_RIGHT: cls.BOTTOM_LEFT,
            cls.TOP_LEFT: cls.BOTTOM_RIGHT,
            cls.BOTTOM_LEFT: cls.TOP_RIGHT,
            cls.BOTTOM_RIGHT: cls.TOP_LEFT,
        }
        return reversed.get(position)


    def get_corresponding_attr(self, position: str):
        if position == self.RIGHT:
            return self.right_node
        elif position == self.TOP_RIGHT:
            return self.top_right_node
        elif position == self.TOP:
            return self.top_node
        elif position == self.TOP_LEFT:
            return self.top_left_node
        elif position == self.LEFT:
            return self.left_node
        elif position == self.BOTTOM_LEFT:
            return self.bottom_left_node
        elif position == self.BOTTOM:
            return self.bottom_node
        elif position == self.BOTTOM_RIGHT:
            return self.bottom_right_node

    def set_to_corresponding_attr(self, position: str, node):
        if position == self.RIGHT:
            self.right_node = node
        elif position == self.TOP_RIGHT:
            self.top_right_node = node
        elif position == self.TOP:
            self.top_node = node
        elif position == self.TOP_LEFT:
            self.top_left_node = node
        elif position == self.LEFT:
            self.left_node = node
        elif position == self.BOTTOM_LEFT:
            self.bottom_left_node = node
        elif position == self.BOTTOM:
            self.bottom_node = node
        elif position == self.BOTTOM_RIGHT:
            self.bottom_right_node = node
        return self.get_corresponding_attr(position)

    def set_relation(self, other_node, position):
        if not self.get_corresponding_attr(position):
            self.set_to_corresponding_attr(position, other_node)
            reversed_position = self.get_reversed_position(position)
            other_node.set_to_corresponding_attr(reversed_position, self)


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

    def find_corresponding_node(self, node, graph2):
        pass

    def compare_graphs(self, graph2):
        pass

    def get_related_info_from_graph(self, graph2):
        pass
