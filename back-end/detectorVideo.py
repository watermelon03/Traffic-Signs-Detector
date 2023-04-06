import cv2
import sys
import time
import json
import numpy as np
import detectorLibrary as DL
import detectorProcess as DP

def getPerTime(startTime, oldTime):
    perTime = time.perf_counter()
    newTime = perTime - startTime
    print(newTime - oldTime)
    oldTime = newTime
    return oldTime

def process2(img, model, outputType, outputShape):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = model(img)
    imgR = cv2.cvtColor(np.squeeze(results.render()), cv2.COLOR_RGB2BGR)
    outputType.write(imgR)
    outputShape.write(imgR)

def yoloDetector(img, model):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = model(img)
    imgR = cv2.cvtColor(np.squeeze(results.render()), cv2.COLOR_RGB2BGR)
    return imgR

def processFull(imgInfo, mode, model, filename, outputType, outputShape):
    frame = imgInfo[0][1].copy()
    imgInfo = DP.shapeDetector(imgInfo, mode)
    imgInfo = DP.colorDetector(imgInfo, mode)
    imgInfo = DP.typeDetector(imgInfo, model)
    accuracy, accurate = DP.generateAccuracy(imgInfo, filename)
    imgInfo, response = DP.generateOutput(imgInfo, accuracy, mode, "all")

    if imgInfo[0][0] == "Yes":
        frameType = imgInfo[0][4]
        outputType.write(frameType)
        outputShape.write(frameType)
    else:
        outputType.write(frame)
        outputShape.write(frame)

def process(imgInfo, mode, model, outputType, outputShape):
    frame = imgInfo[0][1].copy()
    imgInfo = DP.shapeDetector(imgInfo, mode)

    frameType = yoloDetector(frame, model)

    outputType.write(frameType)

    if imgInfo[0][0] == "Yes":
        frameShape = imgInfo[0][3]
        outputShape.write(frameShape)
    else:
        outputShape.write(frame)
        

mode = "test-video"
videoPath = "traffic-sign-detector/back-end/data-test/v5/video/traffic-sign-to-test.mp4"
videoPath2 = "traffic-sign-detector/back-end/data-test/v5/video/Know-Your-Traffic-Signs.mp4"
videoPath3 = "traffic-sign-detector/back-end/data-test/v5/video/699956894_921119.mp4"
videoPath = videoPath3

mode = sys.argv[1]
videoPath = sys.argv[2]

if mode == "test-video":
    startTime = time.perf_counter()
    print("----- Start -----")

model = DL.loadModel(mode)

cap = cv2.VideoCapture(videoPath)

wFrame = int(cap.get(3))
hFrame = int(cap.get(4))

if mode == "test-video":
    filename = videoPath.split("/")[-1]
    prePath = ""
    for i in videoPath.split("/")[0:-1]:
        prePath = prePath + i + "/"
    typeName = filename.split(".")[0] + "_type." + filename.split(".")[1]
    shapeName = filename.split(".")[0] + "_shape." + filename.split(".")[1]

    typePath = prePath + typeName
    shapePath = prePath + shapeName
else:
    typePath = "typeOutput.mp4"
    shapePath  = "shapeOutput.mp4"
    filename = "video"

fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")
outputType = cv2.VideoWriter(typePath, fourcc, 20, (wFrame, hFrame))
outputShape = cv2.VideoWriter(shapePath, fourcc, 20, (wFrame, hFrame))

countFrame = 0
oldTime = 0
while cap.isOpened():
    ret, frame = cap.read()
    if ret == True:
        checkDetector = "No"
        imgInfo = []
        imgInfo.append([checkDetector])

        if mode == "test-video":
            countFrame = countFrame + 1
            print("frame :", countFrame)
            
        imgOri = frame.copy()
        imgInfo[0].append(imgOri)

        processFull(imgInfo, mode, model, filename, outputType, outputShape)
        # process(imgInfo, mode, model, outputType, outputShape)
        # process2(imgOri, model, outputType, outputShape)

        if mode == "test-video":
            oldTime = getPerTime(startTime, oldTime)
    else:
        break

response = {
    "state": True,
    "typePath": typePath,
    "shapePath": shapePath
}

if mode == "test-video":
    endTime = time.perf_counter()
    totalTime = endTime - startTime
    print(totalTime)
    print("finished !!!")

    cap.release()
    outputType.release()
    outputShape.release()
    cv2.destroyAllWindows()

if mode == "web-video":
    print(json.dumps(response))

