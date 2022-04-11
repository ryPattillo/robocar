import cv2 
import numpy as np

def detect_faces(image_name):
    """ finds faces in an image with the name
    image_name
    """

    # read image
    img = cv2.imread(image_name)
    # flip image
    flipped_img = cv2.flip(img,0)
    # convert to gray scale
    gray = cv2.cvtColor(flipped_img, cv2.COLOR_BGR2GRAY)
    # detect faces in image
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # draw rectangle around detect image
    if len(faces) == 0:
        print("NOONE FOUND!")
    else:
        print("A PERSON HAS BEEN DETECTED!")
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    # save the image
    cv2.imwrite("spycam.jpg",img)

def find_shapes(contours):
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
        dim = cv2.approxPolyDP(cnt, 0.005*cnt_len, True)
        # dim = 3 , corresponds to triangle
        if len(dim) == 3 and cv2.contourArea(cnt) > 1000:
            triangles.append(cnt)
        # dim = 4 corresponds to square
        if len(dim) == 4 and cv2.contourArea(cnt) > 1000:
            squares.append(cnt)
    #  return the list of squares and triangles        
    return squares,triangles

def detect_signs(image_name):
    """ Look for signs in the image with name
    image_name
    """

    # read in image
    img = cv2.imread(image_name)
    # flip the image to be right side up
    img = cv2.flip(img,0)
    # convert image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # apply filter to remove noise
    blur_img  = cv2.GaussianBlur(gray_img,(3,3),0)
    # detect edges using Canny
    canny_img = cv2.Canny(blur_img, 100, 200)
    # find the contours in the image
    _,contours,_ = cv2.findContours(canny_img, 
        cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # get the squares and triangles within the image
    squares,triangles = find_shapes(contours)
    # draw shapes on the image
    cv2.drawContours(img, squares, -1, (0, 255, 0), 3)
    cv2.drawContours(img, triangles, -1, (0, 150, 0), 3)
    # get the squares in the image
    cv2.imwrite("signs.jpg",img)

    return len(squares), len(triangles)