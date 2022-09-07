import config

from utils.functions import *

cap = cv2.VideoCapture(config.left_camera, cv2.CAP_DSHOW)
cap2 = cv2.VideoCapture(config.right_camera, cv2.CAP_DSHOW)

setrez(cap)
setrez(cap2)

nr = 0

while cap.isOpened():

    succes1, img = cap.read()
    succes2, img2 = cap2.read()

    k = cv2.waitKey(5)

    cv2.imshow('left cam', img)
    cv2.imshow('right cam', img2)

    if k == config.esc_key:
        break
    elif k == ord(' '):
        cv2.imwrite('images/stereoLeft/imageL' + str(nr) + '.png', img)
        cv2.imwrite('images/stereoRight/imageR' + str(nr) + '.png', img2)
        print("images saved!")
        nr += 1
