import cv2
import numpy as np
from yolov4.tf import YOLOv4

from core.logic.rectangle_graph import YoloRectangle, Point

yolo = YOLOv4()

yolo.config.parse_names("obj.names")
yolo.config.parse_cfg("custom-yolov4-detector.cfg")

yolo.make_model()
yolo.load_weights('./weights/v2/custom_yolov4_v2.weights', weights_type="yolo")
yolo.summary(summary_type="yolo")
yolo.summary()

#yolo.inference(media_path="piia.jpg")
#yolo.get_yolo_detections()

frame = cv2.imread('im4.jpg')
frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
bboxes = yolo.predict(frame_rgb, 0.25)


image = np.copy(frame_rgb)
height, width, _ = image.shape
res_bboxes = bboxes * np.array([width, height, width, height, 1, 1])

print('fuck')
#

kek = [res_bboxes[0], res_bboxes[5]]
for x, y, width, height, _, _ in res_bboxes:
    rec = YoloRectangle(center_point=Point(x, y), width=width, height=height)
    cv2.rectangle(image, (int(rec.point1.x), int(rec.point1.y)), (int(rec.point2.x), int(rec.point2.y)), color=(0, 255, 0), thickness=3)

cv2.imwrite('im41.jpg', image)
#cv2.rectangle(image, (10,10), (100, 100), color=(0, 255, 0), thickness=3)
cv2.imshow('shit', image)
k = cv2.waitKey(0)
# yolo.inference(media_path="road.mp4", is_image=False)
#
# yolo.inference(
#     "/dev/video0",
#     is_image=False,
#     cv_apiPreference=cv2.CAP_V4L2,
#     cv_frame_size=(640, 480),
#     cv_fourcc="YUYV",
# )
