from core.detection.vision_ai.detector import GoogleDetector
from core.detection.yolo.detector import Detector
from core.logic.parse_template import JSONTemplate


class Recognizer:

    @staticmethod
    def recognize_yolo(json_dict: dict, filename):
        image_document_graph = Detector.detect(filename)
        template_graph = JSONTemplate(json_dict)
        template_graph.build_graph()
        res = template_graph.compare(image_document_graph)
        return res

    @staticmethod
    def recognize_visionai(json_dict: dict, filename):
        image_document_graph = GoogleDetector.detect(filename)
        image_document_graph.cleanup()
        template_graph = JSONTemplate(json_dict)
        template_graph.build_graph()
        res = template_graph.compare(image_document_graph)
        return res
