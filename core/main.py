import json
import os
from core.detection.yolo.detector import Detector
from core.logic.parse_template import JSONTemplate

image_path2 = os.path.join(os.path.dirname(__file__), 'detection/yolo/im3.jpg')
image_document_graph = Detector.detect(image_path2)

json_example = json.load(open('logic/v3.json', encoding='utf-8'))


template_graph = JSONTemplate(json_example)
template_graph.build_graph()

#template_graph.compare(img3_graph.graph)

print('Done')
