import os
import cv2
from pprint import pprint
from dataForTest import dataImage

# typeArrayNo = ['No Detect', 'Bend to left', 'Bend to right', 'Fork road', 'No U turn', 
# 'Narrow road', 'No entry', # 'No left turn', 'No right turn', 'Speed limit 30KM', 
# 'Speed limit 50KM', 'Speed limit 60KM', 'Speed limit 70KM', 
# 'Speed limit 80KM', 'Speed limit 90KM', 'Speed limit 100KM', 'Speed limit 120KM']

typeArray = ['No Detect', 'Attention', 'Bend to left', 'Bend to right', 'Cross walk', 'Fork road', 
             'Give way', 'No U turn', 'Narrow road', 'No entry', 'No left turn', 'No right turn', 
             'Roundabout mandatory', 'Speed limit 20KM', 'Speed limit 30KM','Speed limit 40KM', 
             'Speed limit 50KM', 'Speed limit 60KM', 'Speed limit 70KM', 'Speed limit 80KM', 
             'Speed limit 90KM', 'Speed limit 100KM', 'Speed limit 110KM', 'Speed limit 120KM', 'Stop']

shapeArray = ['Triangle', 'Square', 'Rectangle', 'Pentagon', 'Octagon', 'Circle', 'None']

colorArray = ['Black', 'White', 'Red', 'Orange', 'Yellow', 
              'Green', 'Cyan', 'Blue', 'Violet', 'Pink']

clickCount = 0
clickFirst = [False]
clickSecond = [False]

clickEnd = False

def showOption(mode):
    if mode == 't':
        print('Option Type you can choose')
        for i, type in enumerate(typeArray):
            # charB = chr(i+65)
            num = '% s' % i
            print('   ' + num + ' : ' + type)
    elif mode == 's':
        print('Option Shape you can choose')
        for i, shape in enumerate(shapeArray):
            # charL = chr(i+97)
            num = '% s' % i
            print('   ' + num + ' : ' + shape)
    elif mode == 'c':
        print('Option Colors you can choose')
        for i, color in enumerate(colorArray):
            num = '% s' % i
            print('   ' + num + ' : ' + color)
    else:
        print('Incorrect Mode')

def getSelected(value, mode):
    index = int(value)
    selected = 'None'

    if mode == 't':
        if index < len(typeArray):
            selected = typeArray[index]
    elif mode == 's':
        if index < len(shapeArray):
            selected = shapeArray[index]
    elif mode == 'c':
        if index < len(colorArray):
            selected = colorArray[index]
    else:
        selected = 'None'
    return selected

def selectOption():
    showOption('t')
    valueType = input('Enter option type: ')
    typeSelected = getSelected(valueType, 't')

    showOption('s')
    valueShape = input('Enter option shape: ')
    shapeSelected = getSelected(valueShape, 's')

    showOption('c')
    valueColors = input('Enter option color: ')
    valueColorsArray = valueColors.split()
    colorSelected = []
    for i, valueColor in enumerate(valueColorsArray):
        colorSelected.append(getSelected(valueColor, 'c'))

    return typeSelected, shapeSelected, colorSelected

def getGrid(img):
    rows, cols = img.shape[:2]
    size = 100

    for i in range(0, rows, size):
        cv2.line(img, (0, i), (cols, i), (255, 0, 0), 2)

    for i in range(0, cols, size):
        cv2.line(img, (i, 0), (i, rows), (255, 0, 0), 2)

    return img

def getClickEvent(event, x, y, flags, param):
    global clickCount, clickFirst, clickSecond
    if event == cv2.EVENT_LBUTTONDOWN:
        if clickCount == 0:
            clickFirst.append(x)
            clickFirst.append(y)
            clickFirst[0] = True
            print('Yes-top-left, Select point of buttom-right')

        if clickCount == 1:
            clickSecond.append(x)
            clickSecond.append(y)
            clickSecond[0] = True
            print('Yes-buttom-right,  press key n to next')

        clickCount = clickCount + 1


print('Start-Process')

inputNewDir = 'traffic-sign-detector/back-end/data-test/input-new/'
writeDir = 'traffic-sign-detector/back-end/data-test/'

writeName = 'dataForTest.py'
writePath = os.path.join(writeDir, writeName)

# with open(writePath, 'r') as file:
#     exec(file.read())

dataArray = dataImage

for i, nameImage in enumerate(os.listdir(inputNewDir)):
    num = "% s" % i
    path = inputNewDir + nameImage
    inputPath = os.path.join(inputNewDir, nameImage)
    nameImg = int(nameImage.split('.')[0])

    if len(dataArray) != nameImg:
        print(len(dataArray), nameImg)
        print("Error")
        break

    img = cv2.imread(inputPath)
    imgGrid = getGrid(img.copy())

    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', getClickEvent)

    cv2.imshow('Image', imgGrid)

    print('Please any key to continue')
    key = cv2.waitKey(0)

    signCount = int(input('Enter the number of sign: '))

    objectInfoArray = []
    for j in range(signCount):
        signNum = "% s" % j
        nameImgStr = '% s' % nameImg
        print('Please select each option of img-' + signNum + ' of ' + nameImgStr + ' before point image !!!')
        clickCount = 0
        clickFirst = [False]
        clickSecond = [False]

        typeSelected, shapeSelected, colorSelected = selectOption()

        print("Please select point of top-left")

        while(True):
            key = cv2.waitKey(0)
            if key == ord('n') and clickFirst[0] and clickSecond[0]:
                break

        objectInfo = {
            "filename": nameImage,
            "number": j,
            "position": [clickFirst[1], clickFirst[2], clickSecond[1], clickSecond[2]],
            "type": typeSelected,
            "shape": shapeSelected,
            "color": colorSelected
        }
        objectInfoArray.append(objectInfo)

    dataArray.append(objectInfoArray)

    with open(writePath, 'w') as file:
        file.write("dataImage = ")
        pprint(dataArray, file)

    print('Please press key q to next image or press key e to end program')
    while(True):
        key = cv2.waitKey(0)
        if key == ord('q'):
            clickEnd = False
            cv2.destroyAllWindows()
            break
        elif key == ord('e'):
            clickEnd = True
            cv2.destroyAllWindows()
            break
    
    if clickEnd:
        print('You need to end process!')
        break

with open(writePath, 'w') as file:
    file.write("dataImage = ")
    pprint(dataArray, file)

print('End-Process')
