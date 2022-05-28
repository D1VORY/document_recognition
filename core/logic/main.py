import json

import cv2
import numpy as np

from core.logic.rectangle_graph import Point, YoloRectangle, DocumentGraph, RectangleDocumentGraph

bboxes_example = np.load('res_bboxes_example.npy')
# center_x, center_y, width, height, class_id, probability
width = 3014
height = 1993

recs = [
    YoloRectangle(center_point=Point(x, y), width=width, height=height)
    for x, y, width, height, _, _ in bboxes_example
]

rec1, rec2 = recs[0], recs[5]


graph = RectangleDocumentGraph(recs)
graph.build_rectangle_graph()

json_example = json.load(open('v3.json', encoding='utf-8'))

print('Done')
