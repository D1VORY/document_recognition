import cv2
import numpy as np
from yolov4.tf import YOLOv4

yolo = YOLOv4()

yolo.config.parse_names("obj.names")
yolo.config.parse_cfg("custom-yolov4-detector.cfg")

yolo.make_model()
yolo.load_weights('./weights/v2/custom_yolov4.weights', weights_type="yolo")
yolo.summary(summary_type="yolo")
yolo.summary()

yolo.inference(media_path="piia.jpg")
#yolo.get_yolo_detections()

frame = cv2.imread('cum.jpg')
frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
bboxes = yolo.predict(frame_rgb, 0.25)


image = np.copy(frame_rgb)
height, width, _ = image.shape
res_bboxes = bboxes * np.array([width, height, width, height, 1, 1])

print('fuck')
# yolo.inference(media_path="road.mp4", is_image=False)
#
# yolo.inference(
#     "/dev/video0",
#     is_image=False,
#     cv_apiPreference=cv2.CAP_V4L2,
#     cv_frame_size=(640, 480),
#     cv_fourcc="YUYV",
# )
