import cv2
import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'



# Adding custom options
# custom_config = r'--oem 3 --psm 6'
# pytesseract.image_to_string(img, config=custom_config)


# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# noise removal
def remove_noise(image):
    return cv2.medianBlur(image, 5)


# thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


# dilation
def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)


# erosion
def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)


# opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


# canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)


# skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated


# template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)



img = cv2.imread('im1.jpg')
#img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# gray = get_grayscale(img)
# thresh = thresholding(gray)
# opening = opening(gray)
# canny = canny(gray)

# kernel = np.ones((1,1), 'uint8')
# test = img.astype("uint8")
# test = cv2.cvtColor(test, cv2.COLOR_BGR2GRAY)
# test = cv2.dilate(test, kernel, iterations=1)
# test = cv2.erode(test, kernel, iterations=1)
# test = cv2.GaussianBlur(test, (5, 5), 0)
# test = cv2.medianBlur(test, 5)
# #test = cv2.threshold(test, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
# test = cv2.adaptiveThreshold(test, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)


h, w, c = img.shape
#text = pytesseract.image_to_string(img, config='--oem 3 --psm 6', lang='rus')
#print(text)
boxes = pytesseract.image_to_boxes(img, config='--psm 6', lang='rus+eng')
for b in boxes.splitlines():
    b = b.split(' ')
    img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

#print(boxes)
cv2.imwrite('tes_res_rec.jpg', img)
#cv2.imshow('img', img)
#cv2.waitKey(0)
