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

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour = contours[0]
    epsilon = 0.04 * cv2.arcLength(contour, True)
    quad = cv2.approxPolyDP(contour, epsilon, True)
    vertices = quad.reshape(-1, 2)

    xs = sorted(vertices,key = lambda p : p[0])
    ys = sorted(vertices,key = lambda p : p[1])

    tl = []
    tr = []
    bl = []
    br = []

    if np.abs(xs[0][0]-xs[1][0]) < 10 or np.abs(xs[2][0]-xs[3][0]) < 10:
        l = sorted(xs[:2],key = lambda p : p[1])
        tl = l[0]
        bl = l[1]

        r = sorted(xs[2:],key = lambda p : p[1])
        tr = r[0]
        br = r[1]
    elif np.abs(ys[0][1]-ys[1][1]) < 10 or np.abs(ys[2][1]-ys[3][1]) < 10:
        t = sorted(ys[0:2],key = lambda p : p[0])
        tl = t[0]
        tr = t[1]

        b = sorted(ys[2:],key = lambda p : p[0])
        bl = b[0]
        br = b[1]

    stroke = (255,0,0)


    tl = (tl[1],tl[0])
    tr = (tr[1],tr[0])
    bl = (bl[1],bl[0])
    br = (br[1],br[0])

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



