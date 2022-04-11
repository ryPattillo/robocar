from email.mime import image
import cv2 
import numpy as np

def find_people():
    img = cv2.imread('test.jpg')
    img = cv2.flip(img,0)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect faces
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Draw rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    # Display the output
    cv2.imwrite("face_detection.jpg",img)

def pre_process(img):

    # convert image to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  
    # apply filter to remove noise
    img  = cv2.GaussianBlur(img,(3,3),0)
    img = cv2.flip(img,0)
    # _,threshold = cv2.threshold(img,200,255,cv2.THRESH_BINARY)

    # detect edges using Canny
    img = cv2.Canny(img, 100, 200)

    return img

def find_squares(contours):

    # keep track of the squares in the image
    squares = []

    # iterate through all the contours
    for cnt in contours:

        # find the arc length
        cnt_len = cv2.arcLength(cnt, True)

        # get the dimensions to check for square
        dim = cv2.approxPolyDP(cnt, 0.05*cnt_len, True)

        if len(dim) == 3 and cv2.contourArea(cnt) > 1500:
            print("Square")
            squares.append(cnt)

    print(len(squares))
    return squares

def detect_signs():

    # read in image
    original_img = cv2.imread("signs.jpg")
    original_img = cv2.flip(original_img,0)

    # pre process the image
    img = pre_process(original_img)
    
    # find the contours in the image
    _,contours,_ = cv2.findContours(img, 
        cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    squares = find_squares(contours)

    cv2.drawContours(original_img, squares, -1, (0, 255, 0), 3)
    # get the squares in the image

    cv2.imwrite("obj_detection.jpg",img)
    if len(squares) != 0:
        return True
    else:
        return False

