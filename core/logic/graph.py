

class Node:
    TOP = 'TOP'
    BOTTOM = 'BOTTOM'
    RIGHT = 'RIGHT'
    LEFT = 'LEFT'
    TOP_RIGHT = 'TOP_RIGHT'
    TOP_LEFT = 'TOP_LEFT'
    BOTTOM_RIGHT = 'BOTTOM_RIGHT'
    BOTTOM_LEFT = 'BOTTOM_LEFT'

    def __init__(self, data):
        self.data = data
        self.right_node = None
        self.left_node = None
        self.top_node = None
        self.bottom_node = None

        self.top_right_node = None
        self.top_left_node = None
        self.bottom_right_node = None
        self.bottom_left_node = None

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


class DocumentGraph:
    def __init__(self, nodes=None):
        self.nodes = nodes or []

    def add_to_graph(self, node: Node):
        self.nodes.append(node)

    def remove_from_graph(self, node: Node):
        pass

    def find_corresponding_node(self, node, graph2):
        pass

    def compare_graphs(self, graph2):
        pass

    def get_related_info_from_graph(self, graph2):
        pass
