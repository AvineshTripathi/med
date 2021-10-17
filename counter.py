import numpy as np
import cv2


def counter():
    cap = cv2.VideoCapture('demo.mp4')
    fgbg = cv2.createBackgroundSubtractorMOG2()
    people=0

    while True:
        ret, frame = cap.read()
        roi=frame[100: 500, 200:500]
        fgmask = fgbg.apply(roi)
        _, fgmask = cv2.threshold(fgmask, 254, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#        cv2.line(roi, pt1=(0, 60), pt2=(500, 60), color=(0, 0, 255), thickness=2, lineType=8, shift=0)
#       cv2.line(roi, pt1=(0, 65), pt2=(500, 65), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 50:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(roi, (x,y), (x + w, y + h), (0, 255, 0), 3)
                xMid=  int((x +(x+w))/2)
                yMid=  int((y +(y+h))/2)
                if yMid > 60 and yMid < 64:
                    people +=1
                
        cv2.putText(roi, "total people: {}".format(people), (50, 50), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0), 1)
        cv2.imshow('frame', roi)
        cv2.imshow('fgmask',fgmask)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
            
    cap.release()
    cv2.destroyAllWindows()

    return people