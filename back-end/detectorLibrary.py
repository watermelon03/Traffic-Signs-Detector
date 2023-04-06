import os
import cv2
import time
import torch
import numpy as np
import random as rand
import dataForTest as DFT

colorArray = ['Black', 'White', 'Red1', 'Red2', 'Orange', 'Yellow', 
'Green', 'Cyan', 'Blue', 'Violet', 'Pink']

typeArray = ['No Detect', 'Attention', 'Bend to left', 'Bend to right', 'Cross walk', 'Fork road', 
             'Give way', 'No U turn', 'Narrow road', 'No entry', 'No left turn', 'No right turn', 
             'Roundabout mandatory', 'Speed limit 20KM', 'Speed limit 30KM','Speed limit 40KM', 
             'Speed limit 50KM', 'Speed limit 60KM', 'Speed limit 70KM', 'Speed limit 80KM', 
             'Speed limit 90KM', 'Speed limit 100KM', 'Speed limit 110KM', 'Speed limit 120KM', 'Stop']

classArray = ['Attention', 'Bend to left', 'Bend to right', 'Cross walk', 'Fork road', 
             'Give way', 'Narrow road', 'No entry', 'No left turn', 'No right turn', 'No U turn', 
             'Roundabout mandatory', 'Speed limit 100KM', 'Speed limit 110KM', 'Speed limit 120KM',
             'Speed limit 20KM', 'Speed limit 30KM','Speed limit 40KM', 'Speed limit 50KM', 
             'Speed limit 60KM', 'Speed limit 70KM', 'Speed limit 80KM', 'Speed limit 90KM', 'Stop']

def loadModelOld():
    arrayModel = []
    # model = torch.hub.load('dataset-yolov5/traffic-project1/yolov5', 'custom', 'dataset-yolov5/traffic-project1/yolov5/runs/train/exp/weights/best.pt', source='local', force_reload=True)
    for i in range(1):
        i = 3
        if(i == 0):
            # traffic-combined
            model = torch.hub.load('dataset-yolov5/traffic-combined/yolov5', 'custom', 'dataset-yolov5/traffic-combined/yolov5/runs/train/exp/weights/best.pt', source='local', force_reload=True)
        elif(i == 1):
            # traffic-road
            model = torch.hub.load('dataset-yolov5/traffic-road/yolov5', 'custom', 'dataset-yolov5/traffic-road/yolov5/runs/train/exp/weights/best.pt', source='local', force_reload=True)
        elif(i == 2):
            # traffic-project
            model = torch.hub.load('dataset-yolov5/traffic-project1/yolov5', 'custom', 'dataset-yolov5/traffic-project1/yolov5/runs/train/exp/weights/best.pt', source='local', force_reload=True)
        elif(i == 3):
            # traffic-object
            modelPath = 'dataset-yolov5/traffic-object/yolov5'
            model = torch.hub.load(modelPath, 'custom', modelPath + '/runs/train/exp/weights/best.pt', source='local', force_reload=True)
            # model = torch.hub.load('traffic-sign-detector/back-end/dataset-yolov5/traffic-object/yolov5', 'custom', 'traffic-sign-detector/back-end/dataset-yolov5/traffic-object/yolov5/runs/train/exp/weights/best.pt', source='local', force_reload=True)
        elif(i == 4):
            # traffic-sign-dataset
            model = torch.hub.load('dataset-yolov5/traffic-sign-dataset/yolov5', 'custom', 'dataset-yolov5/traffic-sign-dataset/yolov5/runs/train/exp/weights/best.pt', source='local', force_reload=True)
        elif(i == 6):
            # traffic-sign-dataset
            model = torch.hub.load('dataset-yolov5/traffic-sign-dataset3/yolov5', 'custom', 'dataset-yolov5/traffic-sign-dataset3/yolov5/runs/train/exp/weights/best.pt', source='local', force_reload=True)
        arrayModel.append(model)
    # print('Loaded..')
    return arrayModel

def loadModel(mode):
    version = 3
    if version == 1:
        modelPath = "dataset-yolov5/traffic-object/yolov5"
    elif version == 2:
        modelPath = "dataset-yolov5/traffic-sign-dataset3/yolov5"
    elif version == 3:
        modelPath = "dataset-yolov5/traffic-sign-dataset-new/yolov5"
    elif version == 4:
        modelPath = "dataset-yolov5/traffic-sign-dataset-crop/yolov5"
    
    if "test" in mode:
        modelPath = "traffic-sign-detector/back-end/" + modelPath
    model = torch.hub.load(modelPath, 'custom', modelPath + '/runs/train/exp/weights/best.pt', source='local', force_reload=True)
        
    return model

def getBestSize(img):
    try:
        h, w, c = img.shape
    except:
        return 0, 0
    
    if h > 0 and w > 0:
        # increase size
        while w < 570:            
            h = int(h*1.3)
            w = int(w*1.3)
        while h < 550:
            h = int(h*1.3)
            w = int(w*1.3)
        # decrease size
        while w > 920:
            h = int(h/1.2)
            w = int(w/1.2)
        while h > 760:
            h = int(h/1.2)
            w = int(w/1.2)
    return h, w

def getBGR(color):
    # return BGR color
    if color == 'Black':
        BGR = (0,0,0)
    elif color == 'White':
        BGR = (255,255,255)
    elif color == 'Red1':
        BGR = (0,0,255)
    elif color == 'Red2':
        BGR = (0,0,255)
    elif color == 'Orange':
        BGR = (0,153,255)
    elif color == 'Yellow':
        BGR = (0,210,255)
    elif color == 'Green':
        BGR = (0,255,0)
    elif color == 'Cyan':
        BGR = (255,200,50)
    elif color == 'Blue':
        BGR = (255,0,0)
    elif color == 'Violet':
        BGR = (255,100,153)
    elif color == 'Pink':
        BGR = (153,100,255)
    return BGR

def getColor(color, state):
    if color == 'Black':
        lower = np.array([0, 0, 0]) 
        upper = np.array([179, 255, 65])
        BGR = (0,0,0)
    elif color == 'White':
        lower = np.array([0, 0, 175]) 
        upper = np.array([179, 55, 255])
        BGR = (255,255,255)
    elif color == 'Red1':
        lower = np.array([0, 61, 71]) 
        upper = np.array([7, 255, 255])
        BGR = (0,0,255)
    elif color == 'Red2':
        lower = np.array([171, 61, 71]) 
        upper = np.array([179, 255, 255])
        BGR = (0,0,255)
    elif color == 'Orange':
        lower = np.array([8, 61, 71]) 
        upper = np.array([20, 255, 255])
        BGR = (0,153,255)
    elif color == 'Yellow':
        lower = np.array([21, 61, 71]) 
        upper = np.array([40, 255, 255])
        BGR = (0,210,255)
    elif color == 'Green':
        lower = np.array([41, 61, 71]) 
        upper = np.array([90, 255, 255])
        BGR = (0,255,0)
    elif color == 'Cyan':
        lower = np.array([91, 61, 71]) 
        upper = np.array([100, 255, 255])
        BGR = (255,200,50)
    elif color == 'Blue':
        lower = np.array([101, 61, 71]) 
        upper = np.array([130, 255, 255])
        BGR = (255,0,0)
    elif color == 'Violet':
        lower = np.array([131, 61, 71]) 
        upper = np.array([150, 255, 255])
        BGR = (255,100,153)
    elif color == 'Pink':
        lower = np.array([151, 61, 71]) 
        upper = np.array([170, 255, 255])
        BGR = (153,100,255)

    if state == "low-up":
        return lower, upper
    elif state == "BGR":
        return BGR
    else:
        return 0        

def getMask(img, imgHSV):
    imgMaskArray = []

    for color in colorArray:
        # get mask for each color
        lower, upper = getColor(color, "low-up")
        imgMask = cv2.inRange(imgHSV, lower, upper)
        imgMaskArray.append(imgMask)
    return imgMaskArray

def getCannyWithAutoThres(img):
    m = np.median(img)
    t1 = int(max(50, 0.6*m))
    t2 = int(min(190, 1.3*m))
    
    imgCanny = cv2.Canny(img, t1, t2, apertureSize=7)
    # imgCanny = cv2.Canny(img, t1, t2, L2gradient=True)
    # imgCanny = cv2.Canny(img, t1, t2, apertureSize=7, L2gradient=True)

    # thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[0]
    # if isinstance(thresh, np.ndarray):
    #     thresh = thresh.item()
    # imgCanny = cv2.Canny(img, float(thresh*0.5), float(thresh), apertureSize=7, L2gradient=True)

    # img = cv2.bilateralFilter(img, 9, 75, 75)
    # imgCanny = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    # _, imgCanny = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return imgCanny

def getShape(conner, w, h):
    shapeType = "Empty"
    if w < 25 or h < 25:
        return shapeType
    
    if conner == 3 :
        shapeType = "Triangle"
    elif conner == 4:
        ratio = w/float(h)
        if ratio > 0.95 and ratio < 1.05:
            shapeType = "Square"
        else :
            shapeType = "Rectangle"
    elif conner == 5:
        shapeType = "Pentagon"
    elif conner == 8:
        shapeType = "Octagon" 
    elif conner > 6 and conner < 10:
        shapeType = "Circle"
    else:
        shapeType = "None"
    return shapeType

def getRandomNum():
    ran = rand.random()
    seed = rand.randint(10, 20)
    count = rand.randint(0, 9)
    ran = ran * 15

    if ran <= 0 :
        ran = ran + seed
    for i in range(count):
        if i%2 == 0:
            ran = ran + seed - 5
        else:
            ran = ran - seed + 10
    if ran > 35:
        ran = ran - count - 5
    if ran <= 5:
        ran = seed + count*3 + int(ran/3)*15 - 6
    return int(ran)

def checkBorder(mode, num, pair):
    if mode == 'L':
        if num < pair:
            num = pair
    if mode == 'G':
        if num > pair:
            num = pair
    return num

def getShapeContour(imgDil, imgOri, imgInfo):
    i = 0
    checkDetector = "No"
    imgContour = imgOri.copy()
    imgShDet = imgOri.copy()
    hImg, wImg, cImg = imgShDet.shape
    contours, hierarchy = cv2.findContours(imgDil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)        #find contours in img

    for contour in contours:
        area = cv2.contourArea(contour)
        # draw blue contour in all shape
        cv2.drawContours(imgContour, contour, -1, (255,0,0), 2)
        if area > 2200 :
            checkDetector = "Yes"
            # draw red contour in shape if area more than 350
            cv2.drawContours(imgContour, contour, -1, (0,0,255), 2)
            # perimeter of shape
            peri = cv2.arcLength(contour, True)
            # make contour smoooth
            approx = cv2.approxPolyDP(contour, 0.03*peri, True)
            # count conner
            conner = len(approx)
                                          
            x, y, w, h = cv2.boundingRect(approx)
            info = [x, y, w, h]
            xEnd = x+w
            yEnd = y+h
            xCenter = x+(w//2)
            yCenter = y+(h//2)

            shapeType = getShape(conner, w, h)

            if shapeType != "Empty" :                
                xAdd = int(0.45*w)
                yAdd = int(0.45*h)
                
                xLeft = checkBorder('L', x-xAdd, 0)
                xRight = checkBorder('G', xEnd+xAdd, wImg)
                yTop = checkBorder('L', y-yAdd, 0)
                yDown = checkBorder('G', yEnd+yAdd, hImg)

                # get infomation in array
                imgInfo.append([i])
                i = i + 1
                imgInfo[i].append(imgOri[yTop:yDown, xLeft:xRight])
                imgInfo[i].append(info)
                imgInfo[i].append(shapeType)

            numseq = "% s" % conner
            textShape = numseq + '_' + shapeType

            font = cv2.FONT_HERSHEY_COMPLEX
            fontScale = 0.5
            fontThickness = 2
            
            cv2.rectangle(imgShDet, (x,y), (xEnd,yEnd), (0,255,0), 2)
            # ran = getRandomNum()
            # cv2.putText(imgShDet, textShape, (xCenter-ran, yCenter-ran), font, fontScale, (0,0,0), fontThickness)
            
            textSize, baseline = cv2.getTextSize(textShape, font, fontScale, fontThickness)
            hBox = baseline + textSize[1] + 7
            wBox = textSize[0] + 10
            yText = checkBorder('L', y-hBox, 0)
            xText = checkBorder('G', x+wBox, wImg)

            cv2.rectangle(imgShDet, (x, yText), (xText, yText+hBox), (0,220,0), -1)
            cv2.putText(imgShDet, textShape, (x+5, yText+hBox-baseline), font, fontScale, (0,0,0), fontThickness)
    
    imgInfo[0].append(imgContour)
    if checkDetector == 'Yes':
        imgInfo[0][0] = checkDetector
        imgInfo[0].append(imgShDet)

    return imgInfo

def getColorContour(imgMask, imgContour, imgCoDet, setColor, color):
    hImg, wImg, cImg = imgCoDet.shape
    xBorder = int(0.20*wImg)
    yBorder = int(0.20*hImg)

    contours, hierarchy = cv2.findContours(imgMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    BGR = getColor(color, "BGR")
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 27500 :
            # perimeter of shape
            peri = cv2.arcLength(contour, True)
            # make contour smoooth
            approx = cv2.approxPolyDP(contour, 0.03*peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            xEnd = x+w
            yEnd = y+h
            xCenter = x+(w//2)
            yCenter = y+(h//2)

            # check position center of color
            if xCenter <= xBorder or xCenter >= wImg-xBorder :
                continue
            if yCenter <= yBorder or yCenter >= hImg-yBorder :
                continue

            # draw red contour in shape if area more than 30000
            cv2.drawContours(imgContour, contour, -1, (0,0,255), 3)
            checkDetetor = "Yes"
            setColor[0] = checkDetetor
            if color == 'Red1' or color == 'Red2' or color == 'Pink':
                color = 'Red'
            if color == 'Cyan' or color == 'Violet':
                color = 'Blue'

            if color not in setColor:
                setColor.append(color)

            font = cv2.FONT_HERSHEY_COMPLEX
            fontScale = 0.5
            fontThickness = 2

            cv2.rectangle(imgCoDet, (x, y), (xEnd, yEnd), (0,220,0), 3)
            # ran = getRandomNum()
            # cv2.putText(imgOut, textType, (xCenter-ran, yCenter-ran), font, fontScale, (0,0,0), fontThickness)
            
            textSize, baseline = cv2.getTextSize(color, font, fontScale, fontThickness)
            hBox = baseline + textSize[1] + 7
            wBox = textSize[0] + 10
            yText = checkBorder('L', y-hBox, 0)
            xText = checkBorder('G', x+wBox, wImg)

            cv2.rectangle(imgCoDet, (x, yText), (xText, yText+hBox), (0,220,0), -1)
            cv2.putText(imgCoDet, color, (x+5, yText+hBox-baseline), font, fontScale, (0,0,0), fontThickness)

    return imgContour, imgCoDet

def getTypeTrafficOld(type):
    trafficType = 'No Detect'
    if 'no' in type[0]:
        return trafficType
    try:
        textType = type[1]
    except:
        return trafficType

    if 'Bend_to_le' in textType:
        trafficType = 'Bend to left'
    elif 'Bend_to_ri' in textType:
        trafficType = 'Bend to right'
    elif 'Fork_ro' in textType:
        trafficType = 'Fork road'
    elif 'No_u_tu' in textType:
        trafficType = 'No U turn'
    elif 'Narrow' in textType:
        trafficType = 'Narrow road'
    elif 'No_ent' in textType:
        trafficType = 'No entry'
    elif 'No_le' in textType:
        trafficType = 'No left turn'
    elif 'No_ri' in textType:
        trafficType = 'No right turn'
    elif 'Speed_limit_30' in textType:
        trafficType = 'Speed limit 30KM'
    elif 'Speed_limit_50' in textType:
        trafficType = 'Speed limit 50KM'
    elif 'Speed_limit_60' in textType:
        trafficType = 'Speed limit 60KM'
    elif 'Speed_limit_70' in textType:
        trafficType = 'Speed limit 70KM'
    elif 'Speed_limit_80' in textType:
        trafficType = 'Speed limit 80KM'
    elif 'Speed_limit_90' in textType:
        trafficType = 'Speed limit 90KM'
    elif 'Speed_limit_100' in textType:
        trafficType = 'Speed limit 100KM'
    elif 'Speed_limit_120' in textType:
        trafficType = 'Speed limit 120KM'
    return trafficType 

def getTypeTrafficOld2(type):
    index = 0
    if 'no' in type[0]:
        trafficType = typeArray[index]
        return trafficType
    try:
        textType = type[1]
    except:
        trafficType = typeArray[index]
        return trafficType

    if 'Attent' in textType:
        index = 1
    elif 'Bend_to_le' in textType:
        index = 2
    elif 'Bend_to_ri' in textType:
        index = 3
    elif 'Crossw' in textType:
        index = 4
    elif 'Fork_ro' in textType:
        index = 5
    elif 'Give_' in textType:
        index = 6
    elif 'No_u_tu' in textType:
        index = 7
    elif 'Narrow_' in textType:
        index = 8
    elif 'No_ent' in textType:
        index = 9
    elif 'No_lef' in textType:
        index = 10
    elif 'No_rig' in textType:
        index = 11
    elif 'Roundabout_m' in textType:
        index = 12
    elif 'Speed_limit_20' in textType:
        index = 13
    elif 'Speed_limit_30' in textType:
        index = 14
    elif 'Speed_limit_40' in textType:
        index = 15
    elif 'Speed_limit_50' in textType:
        index = 16
    elif 'Speed_limit_60' in textType:
        index = 17
    elif 'Speed_limit_70' in textType:
        index = 18
    elif 'Speed_limit_80' in textType:
        index = 19
    elif 'Speed_limit_90' in textType:
        index = 20
    elif 'Speed_limit_100' in textType:
        index = 21
    elif 'Speed_limit_110' in textType:
        index = 22
    elif 'Speed_limit_120' in textType:
        index = 23
    elif 'St' in textType:
        index = 24

    trafficType = typeArray[index]
    return trafficType 

def getTypeTrafficOld3(type, classes, conf):
    indexMax = 0
    maxConf = -1
    for i in range(len(conf)):
        if conf[i] > maxConf:
            maxConf = conf[i]
            indexMax = i
    
    index = 0
    if indexMax == 0 and 'no' in type[indexMax]:
        trafficType = typeArray[index]
        return trafficType
    try:
        textType = type[(indexMax*2) + 1]
    except:
        trafficType = typeArray[index]
        return trafficType

    if 'Attent' in textType:
        index = 1
    elif 'Bend_to_le' in textType:
        index = 2
    elif 'Bend_to_ri' in textType:
        index = 3
    elif 'Crossw' in textType:
        index = 4
    elif 'Fork_ro' in textType:
        index = 5
    elif 'Give_' in textType:
        index = 6
    elif 'No_u_tu' in textType:
        index = 7
    elif 'Narrow_' in textType:
        index = 8
    elif 'No_ent' in textType:
        index = 9
    elif 'No_lef' in textType:
        index = 10
    elif 'No_rig' in textType:
        index = 11
    elif 'Roundabout_m' in textType:
        index = 12
    elif 'Speed_limit_20' in textType:
        index = 13
    elif 'Speed_limit_30' in textType:
        index = 14
    elif 'Speed_limit_40' in textType:
        index = 15
    elif 'Speed_limit_50' in textType:
        index = 16
    elif 'Speed_limit_60' in textType:
        index = 17
    elif 'Speed_limit_70' in textType:
        index = 18
    elif 'Speed_limit_80' in textType:
        index = 19
    elif 'Speed_limit_90' in textType:
        index = 20
    elif 'Speed_limit_100' in textType:
        index = 21
    elif 'Speed_limit_110' in textType:
        index = 22
    elif 'Speed_limit_120' in textType:
        index = 23
    elif 'St' in textType:
        index = 24
    trafficType = typeArray[index]
    trafficClass = classArray[classes[indexMax]]
    
    # if trafficType != trafficClass:
    #     print(index, indexMax, classes[indexMax])
    #     print(trafficType, trafficClass)
    #     return typeArray[0]
    
    return trafficClass

def getTypeTraffic(classes, conf, area, imgCenter):
    indexMax = -1
    maxConf = -1
    for i in range(len(conf)):
        checkX = (imgCenter[0] > area[i][0]-25 and imgCenter[0] < area[i][2]+25)
        checkY = (imgCenter[1] > area[i][1]-25 and imgCenter[1] < area[i][3]+25)
        if checkX and checkY and conf[i] > maxConf:
            maxConf = conf[i]
            indexMax = i
    
    index = 0
    if indexMax == -1:
        trafficType = typeArray[index]
        return trafficType

    trafficClass = classArray[classes[indexMax]]
    
    return trafficClass

def getYolov5Old(imgOri, arrayModel, imgInfo, seq):
    for i in range(1):
        imgModel = imgOri.copy()
        model = arrayModel[i]

        # config model 
        model.conf = 0.28  # confidence threshold (0-1)
        model.iou = 0.45  # NMS IoU threshold (0-1)
        model.classes = None  # (optional list) filter by class, i.e. = [0, 15, 16] for persons, cats and dogs

        # Inference
        results = model(imgModel)
    
        # print message 
        strResults = str(results)
        listResults = list(strResults.split("\n"))
        listType = list(str(listResults[0])[19:-1].split(" "))

        if listType[0] == '':
            listType.pop(0)

        trafficType = getTypeTraffic(listType)
        if trafficType != 'Stop' and imgInfo[seq][3] == 'Octagon':
            imgInfo[seq][3] = 'Circle'

        imgYolo = np.squeeze(results.render())

    # get infomation in array 
    imgInfo[seq].append(imgYolo)
    imgInfo[seq].append(trafficType)
    return imgInfo

def getYolov5(imgOri, model, imgInfo, seq):
    # startTime = time.perf_counter()
    imgModel = imgOri.copy()
    h, w, c = imgModel.shape
    imgCenter = [(w//2), (h//2)]
    # print(imgCenter)
    
    # cv2.imshow("ImgModel", imgModel)
    # cv2.imwrite("imgModel.jpg", imgModel)

    # config model 
    model.conf = 0.40  # confidence threshold (0-1)
    model.iou = 0.50  # NMS IoU threshold (0-1)
    model.classes = None  # (optional list) filter by class, i.e. = [0, 15, 16] for persons, cats and dogs
    imgModel = cv2.cvtColor(imgModel, cv2.COLOR_BGR2RGB)
    # Inference
    results = model(imgModel)
    
    # print message 
    strResults = str(results)
    listResults = list(strResults.split("\n"))
    listType = list(str(listResults[0])[19:-1].split(" "))
    infoResults = results.xyxy[0]
    
    # print(listType)
    # print(results.xyxy)

    if listType[0] == '':
        listType.pop(0)
    
    listClass = []
    listConf = []
    listArea = []
    if len(infoResults) > 0:
        for i in range(int(len(infoResults))):
            listClass.append(int(infoResults[i][-1]))
            listConf.append(float(infoResults[i][-2]))
            area = []
            for j in range(4):
                area.append(int(infoResults[i][j]))
            listArea.append(area)

    # trafficType = getTypeTrafficOld2(listType)
    trafficType = getTypeTraffic(listClass, listConf, listArea, imgCenter)
    if trafficType != 'Stop' and imgInfo[seq][3] == 'Octagon':
        imgInfo[seq][3] = 'Circle'

    imgYolo = np.squeeze(results.render())
    imgYolo = cv2.cvtColor(imgYolo, cv2.COLOR_RGB2BGR)
        
    # get infomation in array 
    imgInfo[seq].append(imgYolo)
    imgInfo[seq].append(trafficType)

    return imgInfo

def getRect(imgOut, imgInfo, seq, mode):
    hImg, wImg, cImg = imgOut.shape
    x, y, w, h = imgInfo[seq][2]
    shape = imgInfo[seq][3]
    trafficType = imgInfo[seq][7]
    
    xEnd = x+w
    yEnd = y+h
    xCenter = x+(w//2)
    yCenter = y+(h//2)

    xLeft = checkBorder('L', x-15, 0)
    xRight = checkBorder('G', xEnd+15, wImg)
    yTop = checkBorder('L', y-15, 0)
    yDown = checkBorder('G', yEnd+15, hImg)

    numseq = "% s" % seq
    if mode == "test-video" or mode == "web-video":
        textType = trafficType + " / " + shape
    else:
        textType = numseq + " " + trafficType

    font = cv2.FONT_HERSHEY_COMPLEX
    fontScale = 0.5
    fontThickness = 2

    cv2.rectangle(imgOut, (xLeft, yTop), (xRight, yDown), (0,220,0), 3)
    # ran = getRandomNum()
    # cv2.putText(imgOut, textType, (xCenter-ran, yCenter-ran), font, fontScale, (0,0,0), fontThickness)
    
    textSize, baseline = cv2.getTextSize(textType, font, fontScale, fontThickness)
    hBox = baseline + textSize[1] + 7
    wBox = textSize[0] + 10
    yText = checkBorder('L', yTop-hBox, 0)
    xText = checkBorder('G', xLeft+wBox, wImg)

    if xText-xLeft != wBox:
        xLeft = wImg - wBox     # xLeft - (xLeft+wBox-wImg)

    cv2.rectangle(imgOut, (xLeft, yText), (xText, yText+hBox), (0,220,0), -1)
    cv2.putText(imgOut, textType, (xLeft+5, yText+hBox-baseline), font, fontScale, (0,0,0), fontThickness)
    
    return imgOut

def getSubObject(imgInfo, seq):
    shape = imgInfo[seq][3]
    colors = imgInfo[seq][5]
    trafficType = imgInfo[seq][7]

    textColor = ''
    for color in colors:
        if color == 'Yes' or color == 'No':
            if color == 'No':
                textColor = textColor + "No detect color"
                break
            continue
        textColor = textColor + color + ' '

    subObject = {
        "Number ": seq,
        "Type ": trafficType,
        "Shape ": shape,
        "Color ": textColor
    }

    return subObject

def calAccuracy(detected, detectedTrue, detectedFalse, actual):
    accuracy = 0 
    tp = detectedTrue
    # fp = detected - detectedTrue
    fp = detectedFalse
    fn = actual - (detectedTrue + detectedFalse)
    if tp+fp+fn != 0:
        accuracy = min(tp/(tp+fp+fn), 1)
    return max(0, accuracy)

def checkPosition(actualPos, detectedPos, img):
    hImg, wImg, cImg = img.shape
    x, y, w, h = detectedPos
    x1, y1, x2, y2 = actualPos
    xAxis = False
    yAxis = False

    xStart = checkBorder('L', x-10, 0)
    yStart = checkBorder('L', y-10, 0)
    xEnd = checkBorder('G', x+w+10, wImg)
    yEnd = checkBorder('G', y+h+10, hImg)

    if x1 > xStart and x1 < xEnd:
        if x2 > xStart and x2 < xEnd:
            xAxis = True
    if y1 > yStart and y1 < yEnd:
        if y2 > yStart and y2 < yEnd:
            yAxis = True

    if xAxis and yAxis:
        return True
    return False

def compareResults(detected, actual, mode):
    detectedTrue = 0
    detectedFalse = 0
    if mode == "s" or mode == "t":
        if detected == actual:
            detectedTrue += 1
        else:
            detectedFalse += 1

    if mode == "c":
        countTrue = 0
        countFalse = 0
        for color in detected:
            if color == 'Yes' or color == 'No':
                continue
            # print(color)
            if color in actual:
                countTrue += 1
            else:
                countFalse += 1
        acc = calAccuracy(len(detected), countTrue, countFalse, len(actual))
        if acc >= 0.33:
            detectedTrue += 1
        else:
            detectedFalse += 1

    return [detectedTrue, detectedFalse]

def getFinalAccurate(newAcc, oldAcc):
    detectedTrue = oldAcc[0]
    detectedFalse = oldAcc[1]
    if newAcc[0] > 0:
        detectedTrue += 1
    elif newAcc[1] > 0:
        detectedFalse += 1
    return [detectedTrue, detectedFalse]

def getAccurate(imgInfo, seq, numName, accurate):
    complete = False
    detectedPos = imgInfo[seq][2]
    detectedShape = imgInfo[seq][3]
    detectedColors = imgInfo[seq][5]
    detectedType = imgInfo[seq][7]

    if detectedShape == "None" and detectedType == "No Detect":
        return accurate, complete

    indexName = int(numName)
    try:
        dataArray = DFT.dataImage[indexName]
    except: 
        dataArray = []
    # print(dataArray)
    shapeAcc = [0, 0]
    colorAcc = [0, 0]
    typeAcc = [0, 0]
    complete = True

    for data in dataArray:
        if numName in data["filename"]:
            actualPos = data["position"]
            if not checkPosition(actualPos, detectedPos, imgInfo[0][1]):
                continue

            actualShape = data["shape"]
            actualColors= data["color"]
            actualType = data["type"]

            shapeAcc = compareResults(detectedShape, actualShape, "s")
            colorAcc = compareResults(detectedColors, actualColors, "c")
            typeAcc = compareResults(detectedType, actualType, "t")

    accurate["shape"] = getFinalAccurate(shapeAcc, accurate["shape"])
    accurate["color"] = getFinalAccurate(colorAcc, accurate["color"])
    accurate["type"] = getFinalAccurate(typeAcc, accurate["type"])

    if len(dataArray) != accurate["actual"]:
        accurate["actual"] = len(dataArray)

    return accurate, complete

