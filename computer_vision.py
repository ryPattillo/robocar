import cv2 
import numpy as np

def find_people():
    # Load the cascade
    # Read the input image
    img = cv2.imread('image.jpeg')
    # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect faces
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Draw rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    # Display the output
    cv2.imwrite("face_detection.jpeg",img)

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

        if len(dim) == 4 and cv2.contourArea(cnt) > 2000:
            print("Square")
            squares.append(cnt)

    print(len(squares))
    return squares

def detect_signs():

    # read in image
    original_img = cv2.imread("image.jpeg")

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

