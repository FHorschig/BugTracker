import cv2

blue_label_template = "templates/blue_label_template.jpg"

def cv2.imread()

def removeLabels(image):
    blue_template = cv2.imread(blue_label_template)
    res = cv2.matchTemplate(image, blue_template, cv2.TM_CCOEFF_NORMED)