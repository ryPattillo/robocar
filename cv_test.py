import cv2
import numpy as np

def find_shapes(img,contours):
    """ Find shapes given contours
    """
    # keep track of the squares in the image
    squares = []
    triangles = []
    # iterate through all the contours
    for cnt in contours:
        # find the arc length
        cnt_len = cv2.arcLength(cnt, True)
        # get the dimensions to check for square
        dim = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
        # dim = 3 , corresponds to triangle
        if len(dim) == 3 and cv2.contourArea(cnt) > 1000:
            triangles.append(cnt)
        # dim = 4 corresponds to square
        if len(dim) == 4 and cv2.contourArea(cnt) > 1000:
            x,y,w,h = cv2.boundingRect(cnt) # offsets - with this you get 'mask'
            print('Average color (BGR): ',np.array(cv2.mean(img[y:y+h,x:x+w])).astype(np.uint8))
            squares.append(cnt)
    #  return the list of squares and triangles        
    return squares,triangles

image_name = "../../../greensign.png"

# read in image
img = cv2.imread(image_name)
# flip the image to be right side up
orig_img = cv2.flip(img,0)

# convert image to grayscale
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img  = cv2.GaussianBlur(img,(3,3),0)
ret, img = cv2.threshold(img,138,255,cv2.THRESH_TOZERO_INV)

# apply filter to remove noise
# detect edges using Canny

# find the contours in the image
contours,_ = cv2.findContours(img, 
    cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# get the squares and triangles within the image
squares,triangles = find_shapes(orig_img,contours)
# draw shapes on the image
cv2.drawContours(orig_img, squares, -1, (0, 255, 0), 3)
cv2.drawContours(orig_img, triangles, -1, (0, 150, 0), 3)
# get the squares in the image
cv2.imwrite("detect.jpg",orig_img)

