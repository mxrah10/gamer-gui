import cv2 as cv
import numpy as np
class circleMaker():
    def make_dot(img, position):
        cv.circle(img,position,10,(0,0,255),thickness=-1)
        cv.imshow("Dog",img)
        cv.waitKey(7000)


img = cv.imread('dog2.jpg')
position = (img.shape[1]//2,img.shape[0]//2)
circleMaker.make_dot(img,position)


#blank = np.zeros((500,500,3), dtype="uint8")

#cv.imshow("Dog", img)



#cv.circle(img,center, 10, (0,0,255), thickness=-1)
#print(img.shape)
#print(center)
#cv.imshow("Dog", img)
#cv.waitKey(15000)

#cv.destroyAllWindows()


