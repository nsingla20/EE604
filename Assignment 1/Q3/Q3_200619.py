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

    if(angle<0):
        angle = angle + 180



    mat = np.array([
        [1, 0, w/2-center[0]],
        [0, 1, h/2-center[1]]
    ])
    img = cv2.warpAffine(img, mat, (h,w), flags=cv2.INTER_LINEAR)

    rot_mat = cv2.getRotationMatrix2D((w/2,h/2), angle, 1.0)
    img = cv2.warpAffine(img, rot_mat, (h,w), flags=cv2.INTER_LINEAR)

    # print(box,angle)

    img = 255 - img

    img = img[int(h/2 - rech/2):int(h/2 + rech/2),int(w/2 - recw/2):int(w/2 + recw/2)]

    cv2.imwrite('n.png',img)

    ############################
    ############################
    ## comment the line below before submitting else your code wont be executed##
    # pass
    # image = cv2.imread(image_path)
    return img

solution('/mnt/common/DATA/Coding/github/EE604/Assignment 1/Q3/test/3_c.png')
