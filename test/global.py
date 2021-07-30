import cv2 
import numpy as np
import urllib.request
from pyzbar import pyzbar
from pyzbar.pyzbar import decode
import serial
import time

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

def write_read(x):
    ser.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = ser.readline()
    return data

def send_cmd(ser, string_send):
    ser.write(string_send)

def format_str(ID, coor_robot, coor_target):
    xr, yr = coor_robot
    xt, yt = coor_target
    string = f"{ID}{xr:03d}{yr:03d}{xt:03d}{yt:03d}"
    return string 

def getQRS(img):
    return [{
        'polygon':QR.polygon,
        'rect':QR.rect,
        'text': QR.data.decode('utf-8')} 
        for QR in pyzbar.decode(img)]

font = cv2.FONT_HERSHEY_SIMPLEX
cv2.namedWindow("Deteccion",cv2.WINDOW_NORMAL)

cam = "http://192.168.205.173:8080/shot.jpg"

while True:
    imgResp=urllib.request.urlopen(cam) 
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img = cv2.imdecode(imgNp, -1)
    for barcode in decode(img):
        print(barcode.data)
        myData=barcode.data.decode('utf-8')
        ID = 2 
        pts = np.array([barcode.polygon],np.int32)
        pts = pts.reshape((-1,1,2))
        pts2=barcode.rect
        
        centrox = ((pts[0][0][0]+pts[2][0][0]))/2
        centroy = ((pts[0][0][1]+pts[2][0][1]))/2
        cv2.polylines(img,[pts],True, (255,0,0),5)

        centrox= int((999/1080)*centrox)
        centroy= int((999/1080)*centroy)

        cv2.putText(img,myData,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,0,255),2)
        centroOtto= [centrox, centroy]
        print(centroOtto)
        string_send=format_str(ID, centroOtto, [520,280])
        print(string_send+'123')
        write_read(string_send+'123')


    cv2.imshow('Deteccion', img)
    if ord('q') == cv2.waitKey(10):
       exit(0)