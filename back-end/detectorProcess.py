import time
import cv2
import numpy as np
import detectorLibrary as DL

def shapeDetector(imgInfo, mainMode):
    imgOri = imgInfo[0][1].copy()

    # imgR = cv2.cvtColor(imgOri, cv2.COLOR_BGR2RGB)
    # cv2.imshow("ImgR", imgR)
    # imgH = cv2.cvtColor(imgOri, cv2.COLOR_RGB2HSV)
    # cv2.imshow("ImgH", imgH)
    # convert to gray color
    imgGray = cv2.cvtColor(imgOri, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("ImgG", imgGray)
    # make blur
    imgBlur = cv2.GaussianBlur(imgGray, (5,5), 1)

    # make canny for edge detect
    imgCanny = DL.getCannyWithAutoThres(imgBlur)

    # make dilate for edge bigger
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
    imgDil = imgCanny.copy()
    
    # get contour
    imgInfo = DL.getShapeContour(imgDil, imgOri, imgInfo)
    
    if imgInfo[0][0] == "Yes" and mainMode == "test-detect":
        # cv2.imshow("ImgOri", imgInfo[0][1])
        cv2.imshow("ImgContour", imgInfo[0][2])
        cv2.imshow("ImgDetShape", imgInfo[0][3])
        cv2.imshow("ImgCanny", imgCanny)

    return imgInfo

def colorDetector(imgInfo, mainMode):
    # loop of img
    for i in range(len(imgInfo)):
        tag = imgInfo[i][0]
        if tag == "Yes":
            continue
        elif tag == "No":
            break
        img = imgInfo[i][1].copy()
        
        # choose and resize img
        h, w = DL.getBestSize(img)
        if h <= 0 or w <= 0:
            continue 
        imgOri = cv2.resize(img, (w, h))
  
        imgContour = imgOri.copy()
        imgCoDet = imgOri.copy()
        imgMaskArray = []
        checkDetetor = "No"
        setColor = []
        setColor.append(checkDetetor)
        
        if mainMode == "test-video":
            imgInfo[i].append(imgCoDet)
            imgInfo[i].append(setColor)
            continue

        # convert to hsv color  
        imgHSV = cv2.cvtColor(imgOri, cv2.COLOR_BGR2HSV)

        # get mask
        imgMaskArray = DL.getMask(imgOri, imgHSV)

        # get contour
        for j, imgMask in enumerate(imgMaskArray):
            imgContour, imgCoDet = DL.getColorContour(imgMask, imgContour, imgCoDet, setColor, DL.colorArray[j])

        # get infomation in array 
        imgInfo[i].append(imgCoDet)
        imgInfo[i].append(setColor)

    return imgInfo

def typeDetector(imgInfo, model):
    # loop of img
    for i in range(len(imgInfo)):
        tag = imgInfo[i][0]
        if tag == "Yes":
            continue
        elif tag == "No":
            break
        img = imgInfo[i][1].copy()

        # choose and resize img
        h, w = DL.getBestSize(img)
        if h <= 0 or w <= 0:
            continue 
        imgOri = cv2.resize(img, (w, h))
        imgInfo = DL.getYolov5(imgOri, model, imgInfo, i)
      
    return imgInfo

def generateAccuracy(imgInfo, filename):
    accuracy = {
        "shape": 0,
        "color": 0,
        "type": 0
    }
    accurate = {
        "detected": 0,
        "shape": [0, 0],
        "color": [0, 0],
        "type": [0, 0],
        "actual": 0
    }
    count = 0
    numName = filename.split(".")[0]
    if not numName.isdigit():
        return accuracy, accurate

    for i in range(len(imgInfo)):
        tag = imgInfo[i][0]
        if tag == "Yes":
            continue
        elif tag == "No":
            return accuracy, accurate
        accurate, complete = DL.getAccurate(imgInfo, i, numName, accurate)

        if complete:
            count += 1

    accurate["detected"] = count

    accuracyShape = DL.calAccuracy(accurate["detected"], accurate["shape"][0], accurate["shape"][1], accurate["actual"])
    accuracyColor = DL.calAccuracy(accurate["detected"], accurate["color"][0], accurate["color"][1], accurate["actual"])
    accuracyType = DL.calAccuracy(accurate["detected"], accurate["type"][0], accurate["type"][1], accurate["actual"])

    accuracy = {
        "shape": accuracyShape,
        "color": accuracyColor,
        "type": accuracyType
    }
    return accuracy, accurate

def generateOutput(imgInfo, accuracy, mainMode, mode):
    imgOut = imgInfo[0][1].copy()
    objectInfo = []

    # loop of img
    for i in range(len(imgInfo)):
        tag = imgInfo[i][0]
        if tag == "Yes":
            continue
        elif tag == "No":
            noObject = {
                "Report": "Can not detect shape in this picture"
            }
            objectInfo.append(noObject)
            break

        imgOut = DL.getRect(imgOut, imgInfo, i, mainMode)

        subObject = DL.getSubObject(imgInfo, i)
        objectInfo.append(subObject)

    imgInfo[0].append(imgOut)
    
    filenameOut = "imgOutput.jpg"
    
    if mode == "one":
        cv2.imwrite(filenameOut, imgOut)
        if mainMode == "test-detect":
            cv2.imshow("ImgOutput", imgOut)

    response = {
        "state": imgInfo[0][0],
        "imagePath": filenameOut,
        "objectInfo": objectInfo,
        "accuracy": accuracy
    }

    return imgInfo, response

def yoloDetector(img, model):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = model(img)
    imgR = cv2.cvtColor(np.squeeze(results.render()), cv2.COLOR_RGB2BGR)
    return imgR

def mainProcess(imgPath, mode):
    if mode == "test-detect":
        startTime = time.perf_counter()
        print("----- Start -----")
    
    model = DL.loadModel(mode)
    if mode == "test-detect":
        loadedTime = time.perf_counter()
        loaded = loadedTime - startTime
        print(loaded)

    checkDetector = "No"
    imgInfo = []
    imgInfo.append([checkDetector])
    filename = imgPath.split("/")[-1]

    imgOri = cv2.imread(imgPath)


    # choose and resize img
    # h, w = DL.getBestSize(imgOri)
    # if h > 0 and w > 0:
    #     imgOri = cv2.resize(imgOri, (w, h))
    imgInfo[0].append(imgOri)
    
    # call function to detect shape
    if mode == "test-detect":
        print('----- Shape Detect Step -----')
    imgInfo = shapeDetector(imgInfo, mode)
    
    # call function to detect color
    if mode == "test-detect":
        print('----- Color Detect Step -----')
    imgInfo = colorDetector(imgInfo, mode)

    # call function to classification
    if mode == "test-detect":
        print('----- Type Detect Step -----')
    imgInfo = typeDetector(imgInfo, model)
    
    # call function to generate accuracy
    if mode == "test-detect":
        print('----- Generate Accuracy Step -----')
    accuracy, accurate = generateAccuracy(imgInfo, filename)
    
    # call function to generate output
    if mode == "test-detect":
        print('----- Generate Output Step -----')
    imgInfo, response = generateOutput(imgInfo, accuracy, mode, "one")

    if mode == "test-detect":
        print(response["objectInfo"])
        endTime = time.perf_counter()
        totalTime = endTime - startTime
        print(totalTime)
        while(True):
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            break

    return response

def mainProcessWithModel(imgPath, mode, model):
    if mode == "test-detect":
        startTime = time.perf_counter()
        print("----- Start -----")
    
    # model = DL.loadModel(mode)
    if mode == "test-detect":
        loadedTime = time.perf_counter()
        loaded = loadedTime - startTime
        print(loaded)

    checkDetector = "No"
    imgInfo = []
    imgInfo.append([checkDetector])
    filename = imgPath.split("/")[-1]

    imgOri = cv2.imread(imgPath)

    # choose and resize img
    h, w = DL.getBestSize(imgOri)
    if h > 0 and w > 0:
        imgOri = cv2.resize(imgOri, (w, h))
    imgInfo[0].append(imgOri)
    
    # call function to detect shape
    if mode == "test-detect":
        print('----- Shape Detect Step -----')
    imgInfo = shapeDetector(imgInfo, mode)
    
    # call function to detect color
    if mode == "test-detect":
        print('----- Color Detect Step -----')
    imgInfo = colorDetector(imgInfo, mode)

    # call function to classification
    if mode == "test-detect":
        print('----- Type Detect Step -----')
    imgInfo = typeDetector(imgInfo, model)
    
    # call function to generate accuracy
    if mode == "test-detect":
        print('----- Generate Accuracy Step -----')
    accuracy, accurate = generateAccuracy(imgInfo, filename)
    
    # call function to generate output
    if mode == "test-detect":
        print('----- Generate Output Step -----')
    imgInfo, response = generateOutput(imgInfo, accuracy, mode, "one")

    if mode == "test-detect":
        print(response["objectInfo"])
        print("----- Press q key to exit -----")
        endTime = time.perf_counter()
        totalTime = endTime - startTime
        print(totalTime)
        while(True):
            key = cv2.waitKey(0)
            if key == ord('q'):
                cv2.destroyAllWindows()
                break

    return response