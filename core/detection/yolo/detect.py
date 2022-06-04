import cv2
import numpy as np
from yolov4.tf import YOLOv4
import pytesseract
import pickle

from core.logic.rectangle_graph import YoloRectangle, Point, RectangleDocumentGraph

yolo = YOLOv4()

yolo.config.parse_names("obj.names")
yolo.config.parse_cfg("custom-yolov4-detector.cfg")

yolo.make_model()
yolo.load_weights('./weights/v3/custom-yolov4-detector_best.weights', weights_type="yolo")


frame = cv2.imread('im3.jpg')
#frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
bboxes = yolo.predict(frame, 0.25)


image = np.copy(frame)
height, width, _ = image.shape
res_bboxes = bboxes * np.array([width, height, width, height, 1, 1])

print('fuck')
#

kek = [res_bboxes[10], res_bboxes[5]]
fst_bbox = res_bboxes[10]
yolo_recs = []
for x, y, width, height, _, _ in res_bboxes:
    rec = YoloRectangle(center_point=Point(x, y), width=width, height=height)
    cv2.rectangle(image, (int(rec.point1.x), int(rec.point1.y)), (int(rec.point2.x), int(rec.point2.y)), color=(0, 255, 0), thickness=3)
    roi = image[rec.bottom_right_point.int_y: rec.top_left_point.int_y, rec.top_left_point.int_x: rec.bottom_right_point.int_x,:]
    text = pytesseract.image_to_string(roi, config='--oem 3 --psm 6', lang='ukr+eng')
    rec.text = text
    yolo_recs.append(rec)

graph = RectangleDocumentGraph(yolo_recs)
graph.build_rectangle_graph()

cv2.imwrite('im3_improved.jpg', image)
pickle.dump(graph, open('im3_graph.pickle', 'wb'))

# cv2.imshow('shit', image)
# cv2.waitKey(0)
