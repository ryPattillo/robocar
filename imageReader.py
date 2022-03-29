import cv2 
import numpy as np

def pre_process(img):

    # convert image to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  
    # apply filter to remove noise
    img  = cv2.GaussianBlur(img,(1,1),0)

    # detect edges using Canny
    img = cv2.Canny(img, 100, 255)

    return img

def find_squares(contours):

    # keep track of the squares in the image
    squares = []

    # iterate through all the contours
    for cnt in contours:

        # find the arc length
        cnt_len = cv2.arcLength(cnt, True)

        # get the dimensions to check for square
        dim = cv2.approxPolyDP(cnt, 0.01*cnt_len, True)

        if len(dim) == 3:
            print("Square")
            squares.append(cnt)

    print(len(squares))
    return squares

def detect_signs():

    # read in image
    original_img = cv2.imread("shapes.png")

    # pre process the image
    img = pre_process(original_img)
    
    # find the contours in the image
    _,contours,_ = cv2.findContours(img, 
        cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # get the squares in the image
    squares = find_squares(contours)
    if len(squares) != 0:
        return True
    else:
        return False
    #cv2.drawContours(original_img, squares, -1, (0, 255, 0), 3)

    #cv2.imshow('Contours', original_img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()