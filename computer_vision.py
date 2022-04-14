import cv2 
import numpy as np
from time import sleep


def detect_faces(image_name):
    """ finds faces in an image with the name
    image_name
    """
    # read image
    img = cv2.imread(image_name)
    # flip image
    img = cv2.flip(img,1)
    # convert to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
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
    cv2.imwrite(image_name,cv2.flip(img,0))

def find_shapes(img, contours):
    """ Find shapes given contours
    """
    # keep track of the squares in the image
    squares = []
    color = None
    sign_found = False
    # iterate through all the contours
    for cnt in contours:
        # find the arc length
        cnt_len = cv2.arcLength(cnt, True)
        # get the dimensions to check for square
        dim = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
        # dim = 4 corresponds to square
        if len(dim) == 4 and cv2.contourArea(cnt) > 5000:
            x,y,w,h = cv2.boundingRect(cnt) # offsets - with this you get 'mask'
        
            if not sign_found:
                color =  np.array(cv2.mean(img[y:y+h,x:x+w])).astype(np.uint8)
                bgr_color = np.uint8([[[color[0],color[1],color[2] ]]])
        
                color = cv2.cvtColor(bgr_color,cv2.COLOR_BGR2HSV)

                yellow = cv2.inRange(color, (25, 50, 70), (35, 255,255))
                green = cv2.inRange(color, (36, 25, 25), (86, 255,255))

                red1 = cv2.inRange(color, (159, 50, 70), (180, 255, 155))
                red2 = cv2.inRange(color, (0, 50, 70), (9, 255, 255))
                red = red1 | red2

                if red[0][0] == 255:
                    squares.append(cnt)
                    sign_found = True
                    color = 0
                    
                elif yellow[0][0] == 255:
                    squares.append(cnt)
                    sign_found = True
                    color = 1

                elif green[0][0] == 255:
                    squares.append(cnt)
                    sign_found = True
                    color = 2

    #  return the list of squares and triangles        
    return squares, color   

# def get_color_contours(orig_img, hsv_img, color):
#     """
#     Used to get hsv masks for each image
#     """
#     print("On current color : ", color)
#     if(color == 'red'):
#         mask1 = cv2.inRange(hsv_img, (159, 50, 70), (180, 255, 155))
#         mask2 = cv2.inRange(hsv_img, (0, 50, 70), (9, 255, 255))
#         mask = mask1 | mask2
#     elif(color == 'green'):
#         mask = cv2.inRange(hsv_img, (36, 25, 25), (86, 255,255))
#     elif(color == 'blue'):
#         mask = cv2.inRange(hsv_img, (110, 50, 50), (130, 255,255))
#     else:
#         mask = cv2.inRange(hsv_img, (25, 50, 70), (35, 255,255))

#     imask = mask > 0
#     color_mask = np.zeros_like(orig_img, np.uint8)
#     color_mask[imask] = orig_img[imask]
#     sleep(2)

#     img = cv2.cvtColor(color_mask, cv2.COLOR_BGR2GRAY)

#     _,contours,_ = cv2.findContours(img, 
#         cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#     squares = find_shapes(orig_img,contours)

#     return squares

def find_contours(img):
    ''' Find the contours using canny
    '''
    # Convert to Gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Blur the image
    blur = cv2.medianBlur(gray, 5)

    # Apply a binary threshold to the image
    thresh =  cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,11)
    cv2.imwrite("test_images/thresh_test.jpg",thresh)
    # Find contours and filter using threshold area
    _,contours,_ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    return contours


def detect_signs(img_name):
    """ Look for signs in the image with name
    image_name
    """

    # flip the image to be right side up
    img = cv2.imread(img_name)
    img = cv2.flip(img,0)
    orig_img = img
    contours =  find_contours(img)
    squares,color =  find_shapes(img,contours)

    if len(squares) > 0:
        cv2.drawContours(orig_img, squares, -1, (0, 255, 0), 3)
        cv2.imwrite("images/sign_map.jpg",orig_img)
        return color
    else:
        return -1
    #hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)



    # red_squares = get_color_contours(img, hsv_img, 'red')
    # yellow_squares = get_color_contours(img, hsv_img, 'yellow')
    # blue_squares = get_color_contours(img, hsv_img, 'blue')
    # green_squares = get_color_contours(img, hsv_img, 'green')

    # ret = 4

    # if len(red_squares) > 0:
    #     cv2.drawContours(img, red_squares, -1, (0, 255, 0), 3)
    #     ret = 0
    # elif len(yellow_squares) > 0:
    #     cv2.drawContours(img, yellow_squares, -1, (0, 255, 0), 3)
    #     ret = 1

    # elif len(blue_squares) > 0:
    #     cv2.drawContours(img, blue_squares, -1, (0, 255, 0), 3)
    #     ret = 2 

    # elif len(green_squares) > 0:
    #     cv2.drawContours(img, green_squares, -1, (0, 255, 0), 3)
    #     ret = 3

    # cv2.imwrite('test_img.jpg', img)
    # return ret