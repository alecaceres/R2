from src.python.Vision.Classifier import getTarget, getPosNorm
import numpy as np
import cv2
import urllib.request

cam = "http://192.168.205.37:8080/shot.jpg"
pos_red, pos_yellow, pos_blue, pos_green = [[(0,0)]*5]*4
while True:
    imgResp=urllib.request.urlopen(cam) 
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img=cv2.imdecode(imgNp,-1)
    pos_red = getTarget(img, pos_red, "RED")
    pos_blue = getTarget(img, pos_blue, "BLUE")
    pos_green = getTarget(img, pos_green, "GREEN")
    pos_yellow = getTarget(img, pos_yellow, "YELLOW")
    result, pts= getPosNorm(img)
    #img, width, length = getContour(img)
    #img= cv2.rectangle(img, start_bound, end_bound, color = (0, 255, 0), thickness=2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    if len(pts): last_known_position = pts
    cv2.imshow("cam",img)
    if ord('q')==cv2.waitKey(10):
        break