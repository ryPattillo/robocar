import cv2 
import numpy as np
from time import sleep

def detect_faces(img_name):
    """ Finds faces in an image
    """
    # Read image
    img = cv2.imread(img_name)
    # Flip image
    img = cv2.flip(img,0)
    # Convert to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Setect faces in image
    face_cascade = cv2.CascadeClassifier('references/haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Draw Box around face
    if len(faces) == 0:
        print("NOBODY IN SIGHT")
    else:
        print("PERSON FOUND, .... SAVING IMAGE")
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            # save the image
            cv2.imwrite('images/spycamera/person.jpg',img)


def get_squares(img, contours):
    """ Find shapes given a list of contours
    """

    # Hold on to squares in image
    squares = []
    # Check to color 
    color = None
    # Flag for checking if sign is found 
    sign_found = False
    # Iterate through all the contours
    for cnt in contours:
        # Find the arc length
        cnt_len = cv2.arcLength(cnt, True)
        # Get the dimensions to check if square
        dim = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
        # dim = 4 corresponds to square, make sure bigger than size
        if len(dim) == 4 and cv2.contourArea(cnt) > 7500:
            # Get a rectangle
            x,y,w,h = cv2.boundingRect(cnt) 
            # Make sure sign has not already been found
            if not sign_found:
                # Get average color
                color =  np.array(cv2.mean(img[y:y+h,x:x+w])).astype(np.uint8)
                # Get bgr array
                bgr_color = np.uint8([[[color[0],color[1],color[2] ]]])
                color = cv2.cvtColor(bgr_color,cv2.COLOR_BGR2HSV)
                # Get color masks
                yellow = cv2.inRange(color, (25, 50, 70), (35, 255,255))
                green = cv2.inRange(color, (36, 25, 25), (86, 255,255))
                red1 = cv2.inRange(color, (159, 50, 70), (180, 255, 155))
                red2 = cv2.inRange(color, (0, 50, 70), (9, 255, 255))
                red = red1 | red2
                # Red sign detected
                if red[0][0] == 255:
                    squares.append(cnt)
                    sign_found = True
                    color = 0
                # Yellow sign detected
                elif yellow[0][0] == 255:
                    squares.append(cnt)
                    sign_found = True
                    color = 1
                # Green sign detected
                elif green[0][0] == 255:
                    squares.append(cnt)
                    sign_found = True
                    color = 2
    #  return the list of squares and triangles        
    return squares, color   


def get_contours(img):
    ''' Find the contours using canny
    '''
    # Convert to Gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Blur the image
    blur = cv2.medianBlur(gray, 5)
    # Apply a adaptive threshold to the image
    thresh =  cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,11)
    # Write to test file for debugging
    cv2.imwrite("test_images/thresh_test.jpg",thresh)
    # Find contours and filter using threshold area
    _,contours,_ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    return contours


def detect_signs(img_name):
    """ Look for signs in the image with name
    image_name
    """
    # Get and flip image right side up
    img = cv2.imread(img_name)
    img = cv2.flip(img,0)
    # Keep original reference ofr reference
    orig_img = img
    contours =  get_contours(img)
    squares,color =  get_squares(img,contours)
    if len(squares) > 0:
        cv2.drawContours(orig_img, squares, -1, (0, 255, 0), 3)
        cv2.imwrite("images/sign_map.jpg",orig_img)
        return color
    else:
        return -1