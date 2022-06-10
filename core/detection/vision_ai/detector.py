from core.logic.graph import DocumentGraph
import numpy as np
import io
import cv2
from google.cloud import vision

from dotenv import load_dotenv

from core.logic.rectangle_graph import Point, GVisionRectangle, RectangleDocumentGraph

load_dotenv('/Users/olexandr/DEV/document_recognition/.env')

client = vision.ImageAnnotatorClient()


class GoogleDetector:
    @classmethod
    def detect(cls, filename, ) -> DocumentGraph:
        with io.open(filename, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.document_text_detection(image=image)
        text_annotations = response.text_annotations
        rectangle_graph = cls.build_rectangle_graph(text_annotations)
        return rectangle_graph.graph

    @staticmethod
    def draw_bounding_boxes(text_annotations, image):
        new_image = np.copy(image)
        height, width, _ = new_image.shape
        for obj in text_annotations:
            #obj:EntityAnnotation
            points = [Point(x=vertex.x, y=vertex.y) for vertex in obj.bounding_poly.vertices]
            rec = GVisionRectangle(*points)
            cv2.rectangle(
                img=new_image,
                pt1=(int(rec.point1.x), int(rec.point1.y)),
                pt2=(int(rec.point2.x), int(rec.point2.y)),
                color=(0, 255, 0),
                thickness=3
            )
        return new_image

    @staticmethod
    def build_rectangle_graph(text_annotations):
        recs = []
        for obj in text_annotations:
            # obj:EntityAnnotation
            points = [Point(x=vertex.x, y=vertex.y) for vertex in obj.bounding_poly.vertices]
            rec = GVisionRectangle(*points, text=obj.description)
            recs.append(rec)
        graph = RectangleDocumentGraph(recs)
        graph.build_rectangle_graph()
        return graph
