import cv2
import numpy as np

from core.logic.rectangle_graph import Point, YoloRectangle, DocumentGraph

bboxes_example = np.load('res_bboxes_example.npy')
# center_x, center_y, width, height, class_id, probability
width = 3014
height = 1993

recs = [
    YoloRectangle(center_point=Point(x, y), width=width, height=height)
    for x, y, width, height, _, _ in bboxes_example
]

#rec1, rec2 = recs[0], recs[1]
rec1, rec2 = recs[0], recs[5]

# a = rec1.get_relative_position(rec2)
# b = rec1.get_distance(rec2)
# c = rec1.get_distance2(rec2)
# print(a)

graph = DocumentGraph(recs)
graph.build_rectangle_graph()
print('Done')
