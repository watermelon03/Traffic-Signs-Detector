import os
import cv2

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

print('Start')

inputDir = 'traffic-sign-detector/back-end/data-test/input'
newDir = 'traffic-sign-detector/back-end/data-test/input-new'
outputDir = 'traffic-sign-detector/back-end/data-test/output'

for i, image in enumerate(os.listdir(inputDir)):
    num = '% s' % (i + 251)
    if i + 251 < 10:
        num = '00' + num
    elif i + 251 < 100:
        num = '0' + num
    path = inputDir + image
    inputPath = os.path.join(inputDir, image)

    imgOri = cv2.imread(inputPath)

    h, w = getBestSize(imgOri)
    if h > 0 and w > 0:
        imgOri = cv2.resize(imgOri, (w, h), interpolation=cv2.INTER_LINEAR)
    
    imgGrid = imgOri.copy()
    rows, cols = imgGrid.shape[:2]
    size = 100

    for j in range(0, rows, size):
        cv2.line(imgGrid, (0, j), (cols, j), (255, 0, 0), 2)

    for j in range(0, cols, size):
        cv2.line(imgGrid, (j, 0), (j, rows), (255, 0, 0), 2)

    newFileName = num + '.jpg'
    newPath = os.path.join(newDir, newFileName)
    cv2.imwrite(newPath, imgOri, [cv2.IMWRITE_JPEG_QUALITY, 90])

    # outputPath = os.path.join(outputDir, newFileName)
    # cv2.imwrite(outputPath, imgGrid)

    print('Finish image ' + num)

print('Finish All')
