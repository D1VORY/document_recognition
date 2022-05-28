from core.logic.rectangle_graph import Rectangle


class Node:
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
        if position == Rectangle.RIGHT:
            return self.right_node
        elif position == Rectangle.TOP_RIGHT:
            return self.top_right_node
        elif position == Rectangle.TOP:
            return self.top_node
        elif position == Rectangle.TOP_LEFT:
            return self.top_left_node
        elif position == Rectangle.LEFT:
            return self.left_node
        elif position == Rectangle.BOTTOM_LEFT:
            return self.bottom_left_node
        elif position == Rectangle.BOTTOM:
            return self.bottom_node
        elif position == Rectangle.BOTTOM_RIGHT:
            return self.bottom_right_node

    def set_to_corresponding_attr(self, position: str, node):
        if position == Rectangle.RIGHT:
            self.right_node = node
        elif position == Rectangle.TOP_RIGHT:
            self.top_right_node = node
        elif position == Rectangle.TOP:
            self.top_node = node
        elif position == Rectangle.TOP_LEFT:
            self.top_left_node = node
        elif position == Rectangle.LEFT:
            self.left_node = node
        elif position == Rectangle.BOTTOM_LEFT:
            self.bottom_left_node = node
        elif position == Rectangle.BOTTOM:
            self.bottom_node = node
        elif position == Rectangle.BOTTOM_RIGHT:
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
