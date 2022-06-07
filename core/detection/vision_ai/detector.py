from core.logic.graph import DocumentGraph
import numpy as np
import io
import os
import pickle
import cv2
# Imports the Google Cloud client library
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
        # cv_image = cv2.imread(filename)
        # cv_image = cls.draw_bounding_boxes(text_annotations, cv_image)
        # cv2.imshow('shit', cv_image)
        # cv2.waitKey(0)
        # for page in response.full_text_annotation.pages:
        #     for block in page.blocks:
        #         print('\nBlock confidence: {}\n'.format(block.confidence))
        #
        #         for paragraph in block.paragraphs:
        #             print('Paragraph confidence: {}'.format(
        #                 paragraph.confidence))
        #
        #             for word in paragraph.words:
        #                 word_text = ''.join([
        #                     symbol.text for symbol in word.symbols
        #                 ])
        #                 print('Word text: {} (confidence: {})'.format(
        #                     word_text, word.confidence))
        #
        #                 for symbol in word.symbols:
        #                     print('\tSymbol: {} (confidence: {})'.format(
        #                         symbol.text, symbol.confidence))

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


# The name of the image file to annotate
# file_name = os.path.abspath('../im3.jpg')
#
# kek = GoogleDetector.detect(file_name)
#
# print('OHH shit')

# Performs label detection on the image file
# response = client.text_detection(image=image)
# labels = response.text_annotations
#
# for obj in labels:
#     print(obj)
#     print('===========')
#
# #pickle.dump(labels, open('google_text_annotations.pickle', 'wb'))
#
# print('Labels:')
# for label in labels:
#     print(label.description)
