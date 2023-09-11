import cv2
import numpy as np

# Usage
def solution(image_path):
    image= cv2.imread(image_path)
    ######################################################################
    ######################################################################
    #####  WRITE YOUR CODE BELOW THIS LINE ###############################

    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)

    xmin = min(np.where(thresh == 255)[0]) + 5
    xmax = max(np.where(thresh == 255)[0]) - 5
    ymin = min(np.where(thresh == 255)[1]) + 5
    ymax = max(np.where(thresh == 255)[1]) - 5

    tl = (xmin,ymin)
    tr = (xmin,ymax)
    bl = (xmax,ymin)
    br = (xmax,ymax)

    if thresh[tl] == 0:
        if thresh[tr] == 0:
            tl = (xmin, min(np.where(thresh[xmin,:] == 255)[0]))
            tr = (xmin, max(np.where(thresh[xmin,:] == 255)[0]))
        else :
            tl = (min(np.where(thresh[:,ymin] == 255)[0]), ymin)
            bl = (max(np.where(thresh[:,ymin] == 255)[0]), ymin)
    elif thresh[tr] == 0:
        tr = (min(np.where(thresh[:,ymax] == 255)[0]), ymax)
        br = (max(np.where(thresh[:,ymax] == 255)[0]), ymax)
    else:
        bl = (xmax, min(np.where(thresh[xmax,:] == 255)[0]))
        br = (xmax, max(np.where(thresh[xmax,:] == 255)[0]))

    stroke = (255,0,0)


    canvas = np.full((600, 600, 3),255 , dtype="uint8")

    if np.all(image[tl] == image[tr]):
        b,g,r = image[tl]
        cv2.rectangle(canvas, (0,0), (600,199), (int(b), int(g), int(r),0), -1,1)
        b,g,r = image[bl]
        cv2.rectangle(canvas, (0,399), (600,600), (int(b), int(g), int(r)), -1)
    else:
        b,g,r = image[tl]
        cv2.rectangle(canvas, (0,0), (199,600), (int(b), int(g), int(r)), -1)
        b,g,r = image[tr]
        cv2.rectangle(canvas, (399,0), (600,600), (int(b), int(g), int(r)), -1)

    cv2.circle(canvas, (299,299), 99, stroke, 2)
    for i in range(24):
        angle = np.deg2rad(i*15)
        x = int(299 + 99*np.cos(angle))
        y = int(299 + 99*np.sin(angle))
        cv2.line(canvas, (299,299), (x,y), stroke,1)

    image = canvas

    ######################################################################

    return image



