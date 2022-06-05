import cv2
import numpy as np
import pytesseract
from yolov4.tf import YOLOv4
import os

from core.logic.graph import DocumentGraph
from core.logic.rectangle_graph import YoloRectangle, Point, RectangleDocumentGraph

TEST_FILENAME = os.path.join(os.path.dirname(__file__), 'weights/v3/custom-yolov4-detector_best.weights')

open(TEST_FILENAME)
yolo = YOLOv4()
yolo.config.parse_names(os.path.join(os.path.dirname(__file__), 'obj.names'))
yolo.config.parse_cfg(os.path.join(os.path.dirname(__file__), 'custom-yolov4-detector.cfg'))
yolo.make_model()
yolo.load_weights(os.path.join(os.path.dirname(__file__), 'weights/v3/custom-yolov4-detector_best.weights'), weights_type="yolo")


class Detector:
    @classmethod
    def detect(cls, filename, prob_thresh=0.5) -> DocumentGraph:
        cv_image = cv2.imread(filename)
        bounding_boxes = yolo.predict(cv_image, prob_thresh=prob_thresh)
        height, width, _ = cv_image.shape
        bounding_boxes = bounding_boxes * np.array([width, height, width, height, 1, 1]) # make matrix to have actual points
        rectangle_graph = cls.build_rectangle_graph(bounding_boxes, cv_image)
        return rectangle_graph.graph

    @staticmethod
    def draw_bounding_boxes(bounding_boxes, image):
        new_image = np.copy(image)
        height, width, _ = new_image.shape
        for x, y, width, height, _, _ in bounding_boxes:
            rec = YoloRectangle(center_point=Point(x, y), width=width, height=height)
            cv2.rectangle(
                img=new_image,
                pt1=(int(rec.point1.x), int(rec.point1.y)),
                pt2=(int(rec.point2.x), int(rec.point2.y)),
                color=(0, 255, 0),
                thickness=3
            )
        return new_image

    @staticmethod
    def build_rectangle_graph(bounding_boxes, image):
        height, width, _ = image.shape
        yolo_recs = []
        for x, y, width, height, _, _ in bounding_boxes:
            rec = YoloRectangle(center_point=Point(x, y), width=width, height=height)
            roi = image[
                  rec.bottom_right_point.int_y: rec.top_left_point.int_y,
                  rec.top_left_point.int_x: rec.bottom_right_point.int_x,
                  :
            ]
            text = pytesseract.image_to_string(roi, config='--oem 3 --psm 6', lang='ukr+eng')
            if not text:
                continue
            rec.text = text
            yolo_recs.append(rec)
        graph = RectangleDocumentGraph(yolo_recs)
        graph.build_rectangle_graph()
        return graph
