import cv2
import numpy as np

def solution(image_path):
    ############################
    ############################

    image = cv2.imread(image_path)
    w,h,c = image.shape
    image = cv2.copyMakeBorder(image, int(h/2), int(h/2), int(w/2), int(w/2), cv2.BORDER_CONSTANT, value=(255,255,255))
    w,h,c = image.shape
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ret,img = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)

    cnt=[]

    for i in range(w):
        for j in range(h):
            if img[i,j] > 0:
                cnt.append([j,i])

    cnt = np.array(cnt)

    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    # box = np.int0(box)

    center = np.average(box,axis=0)
    # cv2.drawContours(img,[box],0,255,2)
    # print(box,center)
    box = box - box[0]


    box = sorted(box,key = lambda p : p[0]**2 + p[1]**2)

    recw = np.sqrt(box[2][1]**2+box[2][0]**2) + 10
    rech = np.sqrt(box[1][1]**2+box[1][0]**2) + 10

    angle = np.rad2deg(np.arctan(box[2][1]/box[2][0]))

    # if(angle<0):
    #     angle = angle + 180



    mat = np.array([
        [1, 0, w/2-center[0]],
        [0, 1, h/2-center[1]]
    ])
    img = cv2.warpAffine(img, mat, (h,w), flags=cv2.INTER_LINEAR)

    rot_mat = cv2.getRotationMatrix2D((w/2,h/2), angle, 1.0)
    img = cv2.warpAffine(img, rot_mat, (h,w), flags=cv2.INTER_LINEAR)

    img1 = np.copy(img)
    img2 = cv2.flip(img1, 0)
    img2 = cv2.flip(img2, 1)

    edges1 = cv2.Canny(img1, 50, 150)
    edges2 = cv2.Canny(img2, 50, 150)

    lines1 = cv2.HoughLines(edges1, 1, np.pi / 180, threshold=100)
    lines2 = cv2.HoughLines(edges2, 1, np.pi / 180, threshold=100)

    avg1 = []
    avg2 = []

    for line in lines1:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        y0 = b * rho
        y1 = int(y0 + 1000 * (a))
        y2 = int(y0 - 1000 * (a))
        avg1.extend([y1,y2])

    for line in lines2:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        y0 = b * rho
        y1 = int(y0 + 1000 * (a))
        y2 = int(y0 - 1000 * (a))
        avg2.extend([y1,y2])

    # avg1 = np.min(avg1)
    # avg2 = np.min(avg2)

    print(avg1, avg2)

    if avg1 < avg2:
        img = img1
    else:
        img = img2

    img = 255 - img

    img = img[int(h/2 - rech/2):int(h/2 + rech/2),int(w/2 - recw/2):int(w/2 + recw/2)]

    ############################
    ############################
    ## comment the line below before submitting else your code wont be executed##
    # pass
    # image = cv2.imread(image_path)
    return img

