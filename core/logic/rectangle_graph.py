import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_distance(self, point):
        return math.sqrt((self.x - point.x)**2 + (self.y - point.y)**2)

class Rectangle:
    TOP = 'TOP'
    BOTTOM = 'BOTTOM'
    RIGHT = 'RIGHT'
    LEFT = 'LEFT'
    TOP_RIGHT = 'TOP_RIGHT'
    TOP_LEFT = 'TOP_LEFT'
    BOTTOM_RIGHT = 'BOTTOM_RIGHT'
    BOTTOM_LEFT = 'BOTTOM_LEFT'


    def __init__(self, point1, point2):
        """
        rectangle on the image

        :param point1: top left point
        :param point2: bottom right point
        """
        if point1.x == point2.x or point1.y == point2.y:
            raise ValueError('fuck you')
        if point1.x > point2.x:
            point1, point2 = point2, point1
        if point1.y < point2.y:
            point1.y, point2.y = point2.y, point1.y

        self.point1 = point1
        self.point2 = point2
        self.length = abs(point2.x - point1.x)
        self.height = abs(point2.y - point1.y)
        self.center = Point((point2.x + point1.x) / 2, (point2.y + point1.y) / 2)

    def get_distance(self, rectangle):
        left = rectangle.point2.x < self.point1.x
        right = self.point2.x < rectangle.point1.x
        bottom = rectangle.point2.y < self.point1.y
        top = self.point2.y < rectangle.point1.y
        if top and left:
            return Point(self.point1.x, self.point2.y).get_distance(Point(rectangle.point2.x, rectangle.point1.y))
        elif left and bottom:
            return self.point1.get_distance(rectangle.point2)
        elif bottom and right:
            return Point(self.point2.x, self.point1.y).get_distance(Point(rectangle.point1.x, rectangle.point2.y))
        elif right and top:
            return self.point2.get_distance(rectangle.point1)
        elif left:
            return self.point1.x - rectangle.point2.x
        elif right:
            return rectangle.point1.x - self.point2.x
        elif bottom:
            return self.point1.y - rectangle.point2.y
        elif top:
            return rectangle.point1.y - self.point2.y
        else:  # rectangles intersect, distance between centers
            return self.center.get_distance(rectangle.center)


    def get_relative_position(self, rect):
        """return relative position of rectangle from object"""
        return self.TOP


class YoloRectangle(Rectangle):
    def __init__(self, center_point, width, height):
        half_width = int(width / 2)
        half_height = int(height / 2)

        top = center_point.x - half_width
        if top < 10:
            top = 10
        left = center_point.y - half_height
        if left < 0:
            left = 0

        top_left = Point(top, left)
        bottom_right = Point(center_point.x + half_width, center_point.y + half_height)
        super().__init__(top_left, bottom_right)


class Node:
    def __init__(self, data):
        self.data = data
        self.right_nodes = []
        self.left_nodes = []
        self.top_nodes = []
        self.bottom_nodes = []

        self.top_right_nodes = []
        self.top_left_nodes = []
        self.bottom_right_nodes = []
        self.bottom_left_nodes = []


class DocumentGraph:

    def __init__(self):
        pass

    def build_rectangle_graph(self):
        pass

    def find_closest_rectangles(self, rectangle):
        pass

