from circleDrawer import circleMaker as cm, circleMaker
import cv2 as cv

img = cv.imread('dog.jpg', 1)
temp = circleMaker(img)
cv.imshow('image', img)
cv.setMouseCallback('image', temp.click_event)
cv.waitKey(0)
cv.destroyAllWindows()