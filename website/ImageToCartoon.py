import cv2
import numpy as np
import matplotlib.pyplot as plt

# img = cv2.imread("1_1.jpg")
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# plt.figure(figsize=(10, 10))
# plt.imshow(img)
# plt.axis("off")
# plt.title("Original Image")
# plt.show()
img = cv2.imread('c0mplex.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.medianBlur(gray, 5)
outline = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                cv2.THRESH_BINARY, 9, 9)

color = cv2.bilateralFilter(img, 9, 250, 250)
cartoon = cv2.bitwise_and(color, color, mask=outline)

cv2.imshow('Original Image', img)
cv2.imshow('Outline', outline)
cv2.imshow('Cartoon', cartoon)
cv2.waitKey(0)
cv2.destroyAllWindows()