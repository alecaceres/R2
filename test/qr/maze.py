import numpy as np
import cv2
import urllib.request
from math import sqrt
from src.python.Vision.QR_reader import getQRS

def getTarget(img, pos, col):
    '''
    col: uno de "YELLOW", "RED", "BLUE" o "GREEN"
    '''
    result = img.copy()
    image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    if col == "RED":
        # lower boundary RED color range values; Hue (0 - 10)
        lower1 = np.array([0, 100, 20])
        upper1 = np.array([10, 255, 255])
        
        # upper boundary RED color range values; Hue (160 - 180)
        lower2 = np.array([160,100,20])
        upper2 = np.array([179,255,255])
        
        lower_mask = cv2.inRange(image, lower1, upper1)
        upper_mask = cv2.inRange(image, lower2, upper2)
        mask = lower_mask + upper_mask
    elif col == "BLUE":
        lower1 = np.array([90, 70, 30])
        upper1 = np.array([134, 255, 255])
        mask = cv2.inRange(image, lower1, upper1)
    elif col == "GREEN":
        lower1 = np.array([40, 40, 40])
        upper1 = np.array([70, 255, 255])
        mask = cv2.inRange(image, lower1, upper1)
    else: # YELLOW
        lower1 = np.array([22, 93, 0])
        upper1 = np.array([35, 255, 255])
        mask = cv2.inRange(image, lower1, upper1)

    mask = remove_noise(mask)
    result = cv2.bitwise_and(result, result, mask=mask)
    centroid = get_centroid(mask)
    pos = [*pos[1:], centroid]
    cX, cY = np.median(np.array(pos), axis = 0)
    cv2.circle(result, (int(cX), int(cY)), 5, (255, 255, 255), -1)

    scale_percent = 60 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    
    # resize image
    result = cv2.resize(result, dim, interpolation = cv2.INTER_AREA)

    cv2.imshow(col, result)
    return pos

def get_centroid(img):
    # calculate moments of binary image
    M = cv2.moments(img)

    if M["m00"] == 0: return 0, 0

    # calculate x,y coordinate of center
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    return cX, cY

def getPosNorm(img):
    result, pts= [], []
    for QR in getQRS(img): # considerando múltiples QR en una imagen
        Cx, Cy = 0, 0 # se inicializan coordenadas del centroide en 0
        for point in QR['polygon']: # se recorren los puntos del polígono del QR
            Cx += point.x
            Cy += point.y
        pts=np.array([[point.x, point.y] for point in QR['polygon']], np.int32).reshape((-1, 1, 2)) if QR['polygon'] else []
        Cx/=4; Cy/=4 # se obtiene el centroide absoluto en la imagen
        result.append(QR["text"])
        print(QR["text"])
    return result, pts

def remove_noise(img):
    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(img, None, None, None, 8, cv2.CV_32S)

    #get CC_STAT_AREA component as stats[label, COLUMN] 
    areas = stats[1:,cv2.CC_STAT_AREA]

    result = np.zeros((labels.shape), np.uint8)

    for i in range(0, nlabels - 1):
        if areas[i] >= 400:   #keep
            result[labels == i + 1] = 255
    return result
    
def getContour(img):
    cv2.imshow('Increased contrast', img)
    #cv2.imwrite('sunset_modified.jpg', img)
    # convertir a escala de grises
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # thresholding binario
    _, thresh = cv2.threshold(img_gray, 110, 255, cv2.THRESH_BINARY)
    # do connected components processing
    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh, None, None, None, 8, cv2.CV_32S)

    #get CC_STAT_AREA component as stats[label, COLUMN] 
    areas = stats[1:,cv2.CC_STAT_AREA]

    result = np.zeros((labels.shape), np.uint8)

    for i in range(0, nlabels - 1):
        if areas[i] >= 2000:   #keep
            result[labels == i + 1] = 255
    cv2.imshow("filtrado", thresh)
    cv2.imshow("sin ruido", result)
    contours, _ = cv2.findContours(image=thresh, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)             
    image_copy = img.copy() # para dibujar sobre la imagen original
    c = max(contours, key = cv2.contourArea) # para obtener el contorno más grande
    # se dibuja en verde el rect. aproximación, ya que la cámara apunta perpendicular al suelo
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(image_copy,contours,0,(0,0,255),2)
    box = [*box, box[0]]
    distances = [sqrt((box[i][0]-box[i+1][0])**2
                    + (box[i][1]-box[i+1][1])**2)
                    for i in range(4)]
    width = min(distances)
    length = max(distances)
    print(int(width), int(length))
    return image_copy, width, length

def func():
    cam = "http://192.168.205.173:8080/shot.jpg"
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
func()
while False:
    #This is to check whether to break the first loop
    isclosed=0
    cap = cv2.VideoCapture(0)
    while (True):
        ret, frame = cap.read()
        # It should only show the frame when the ret is true
        try: frame, width, length = getContour(frame)
        except: pass
        if ret == True:

            cv2.imshow('frame',frame)
            if cv2.waitKey(1) == 27:
                # When esc is pressed isclosed is 1
                isclosed=1
                break
        else:
            break
    # To break the loop if it is closed manually
    if isclosed:
        break



cap.release()
cv2.destroyAllWindows()