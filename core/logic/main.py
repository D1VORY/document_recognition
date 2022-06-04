import json
import pickle

import cv2
import numpy as np

from core.logic.parse_template import JSONTemplate
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
json_example = json.load(open('v3.json', encoding='utf-8'))


img3_graph = pickle.load(open('im3_graph.pickle', 'rb'))

template_graph = JSONTemplate(json_example)
template_graph.build_graph()



print('Done')
