import sys
import os
import time
import cv2
import json
import detectorLibrary as DL
import detectorProcess as DP

mode = "test-acc"

mode = sys.argv[1]

if mode == "test-acc":
    startTime = time.perf_counter()
    print('----- Start-Process -----')

v = 'v5'
if mode == "test-acc":
    inputNewDir = 'traffic-sign-detector/back-end/data-test/' + v + '/input-new/'
    # inputNewDir = 'traffic-sign-detector/back-end/data-test/' + v + '/re/'
    outputDir = 'traffic-sign-detector/back-end/data-test/' + v + '/output-detect/'
    shapeDir = 'traffic-sign-detector/back-end/data-test/' + v + '/output-shape/'
    conDir = 'traffic-sign-detector/back-end/data-test/' + v + '/output-con/'
if mode == "web-acc":
    inputNewDir = 'data-test/' + v + '/input-new/'

model = DL.loadModel(mode)
if mode == "test-acc":
        loadedTime = time.perf_counter()
        loaded = loadedTime - startTime
        print(loaded)

accSumShape = 0
accSumColor = 0
accSumType = 0
count = 0
count2 = 0

for i, image in enumerate(os.listdir(inputNewDir)):
    num = "% s" % i
    path = inputNewDir + image
    inputPath = os.path.join(inputNewDir, image)

    checkDetector = "No"
    imgInfo = []
    imgInfo.append([checkDetector])
    filename = inputPath.split("/")[-1]

    img = cv2.imread(inputPath)
    imgOri = img.copy()
    imgInfo[0].append(imgOri)

    # call function to detect shape
    imgInfo = DP.shapeDetector(imgInfo, mode)

    # call function to detect color
    imgInfo = DP.colorDetector(imgInfo, mode)

    # call function to classification
    imgInfo = DP.typeDetector(imgInfo, model)

    # call function to generate accuracy
    accuracy, accurate = DP.generateAccuracy(imgInfo, filename)

    # call function to generate output
    imgInfo, response = DP.generateOutput(imgInfo, accuracy, mode, "all")
    
    count += 1
    if imgInfo[0][0] == "Yes":
        count2 += 1
        countStr = "% s" % count
        count2Str = "% s" % count2

        accSumShape += accuracy["shape"]
        accSumColor += accuracy["color"]
        accSumType += accuracy["type"]

        if mode == "test-acc":
            imgCon = imgInfo[0][2]
            imgShape = imgInfo[0][3]
            imgOut = imgInfo[0][4]

            # conPath = os.path.join(conDir, image)
            # cv2.imwrite(conPath, imgCon)

            # shapePath = os.path.join( shapeDir, image)
            # cv2.imwrite( shapePath, imgShape)

            # outPath = os.path.join(outputDir, image)
            # cv2.imwrite(outPath, imgOut)

            print(num + "---" + countStr + "---" + count2Str)

accuracyAVG = {
    "shape": round(accSumShape/count2, 3),
    "color": round(accSumColor/count2, 3),
    "type": round(accSumType/count2, 3),
    "countTotal": count,
    "countDetect": count2
}

if mode == "test-acc":
    print("----- End-Process -----")
    print(accuracyAVG)

    endTime = time.perf_counter()
    totalTime = endTime - startTime
    print(totalTime)

if mode == "web-acc":
    print(json.dumps(accuracyAVG))