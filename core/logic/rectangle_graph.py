import math
from typing import List

import numpy as np

from core.logic.graph import Node, DocumentGraph


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_distance(self, point):
        return math.sqrt((self.x - point.x)**2 + (self.y - point.y)**2)

    def get_angle(self, point):
        radius = self.get_distance(point)
        point2 = Point(self.x + radius, self.y)

        vector1 = Point(point2.x - self.x, point2.y - self.y)
        vector2 = Point(point.x - self.x, point.y - self.y)
        vector1_module = vector1.get_distance(Point(0, 0))
        vector2_module = vector2.get_distance(Point(0, 0))

        cos_alpha = (vector1.x * vector2.x + vector1.y * vector2.y) / (vector1_module * vector2_module)
        angle_alpha = math.acos(cos_alpha) * 180 / math.pi
        if point.y > self.y:
            return 360 - angle_alpha
        return angle_alpha

    def __repr__(self):
        return f'{self.x} | {self.y}'


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

    @property
    def top_left_point(self):
        return self.point1

    @property
    def bottom_left_point(self):
        return Point(self.point1.x, self.point2.y)

    @property
    def top_right_point(self):
        return Point(self.point2.x, self.point1.y)

    @property
    def bottom_right_point(self):
        return self.point2

    def get_distance(self, rectangle):
        position = self.get_relative_position(rectangle)
        res = 0
        if position == Node.RIGHT:
            res = rectangle.top_left_point.x - self.top_right_point.x
        elif position == Node.TOP_RIGHT:
            res = self.top_right_point.get_distance(rectangle.bottom_left_point)
        elif position == Node.TOP:
            res = self.top_left_point.y - rectangle.bottom_left_point.y
        elif position == Node.TOP_LEFT:
            res = self.top_left_point.get_distance(rectangle.bottom_right_point)
        elif position == Node.LEFT:
            res = self.top_left_point.x - rectangle.top_right_point.x
        elif position == Node.BOTTOM_LEFT:
            res = self.bottom_left_point.get_distance(rectangle.top_right_point)
        elif position == Node.BOTTOM:
            res = rectangle.top_left_point.y - self.bottom_left_point.y
        elif position == Node.BOTTOM_RIGHT:
            res = self.bottom_right_point.get_distance(rectangle.top_left_point)
        return abs(res)

    def get_relative_position(self, rect):
        """return relative position of rectangle from object"""
        #angle = self.center.get_angle(rect.center)
        angle = self.point1.get_angle(rect.point1)
        if angle <= 22.5 or angle >= 337.5:
            return Node.RIGHT
        elif 67.5 > angle > 22.5:
            return Node.TOP_RIGHT
        elif 112.5 >= angle >= 67.5:
            return Node.TOP
        elif 157.5 > angle > 112.5:
            return Node.TOP_LEFT
        elif 202.5 >= angle >= 157.5:
            return Node.LEFT
        elif 247.5 > angle > 202.5:
            return Node.BOTTOM_LEFT
        elif 292.5 >= angle >= 247.5:
            return Node.BOTTOM
        elif 337.5 > angle > 292.5:
            return Node.BOTTOM_RIGHT


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


class RectangleDocumentGraph:

    def __init__(self, rectangles: List[Rectangle]):
        self.rectangles = rectangles
        self.n = len(rectangles)
        self.distances = np.zeros(shape=(self.n, self.n))
        self.calculate_distances()
        self.graph = DocumentGraph()
        for i in range(self.n):
            node = Node(node_id=i, value=f'{self.rectangles[i].top_left_point} ___ {self.rectangles[i].bottom_right_point}')
            self.graph.add_to_graph(node)

    def build_rectangle_graph(self):
        indeces_of_sorted = np.argsort(self.distances, axis=1)
        for rect_index in range(self.n):
            for dist_index in indeces_of_sorted[rect_index, 1:]:
                position = self.rectangles[rect_index].get_relative_position(self.rectangles[dist_index])
                node = self.graph.get_node_by_id(rect_index)
                other_node = self.graph.get_node_by_id(dist_index)
                node.set_relation(other_node, position)

    def calculate_distances(self):
        for i in range(self.n):
            for j in range(self.n):
                self.distances[i, j] = self.rectangles[i].get_distance(self.rectangles[j])
        return self.distances

