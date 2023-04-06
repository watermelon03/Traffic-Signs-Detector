import sys
import json
import detectorProcess as DP



mode = "test-detect"

# imagePath = "traffic-sign-detector/back-end/data-test/input-new/032.jpg"
# imagePath1 = "traffic-sign-detector/back-end/image/001370_jpg.rf.76af28652eefa88de490db72bc490e69.jpg"
# imagePath2 = "traffic-sign-detector/back-end/image/signs-road-restriction-right-2293.jpg"
# imagePath3 = "traffic-sign-detector/back-end/image/002197_jpg.rf.b5b9d48a20f3888374ca24befa14e6ca.jpg"
imagePath4 = "traffic-sign-detector/back-end/image/10ec6364-6260-4d4d-84d4-ca0d48f991ec.jpg"
imagePath5 = "traffic-sign-detector/back-end/image/istockphoto-962513676-612x612-Kopya_jpg.rf.2d4b18a0f77e5da7282d204011c9837c.jpg"
imagePath6 = "traffic-sign-detector/back-end/dataset-yolov5/traffic-sign-dataset-new/yolov5/Traffic-sign-dataset-7/train/images/-_JPG.rf.f54615c97101816c3075b9c4b7b1e84f.jpg"
imagePath7 = "traffic-sign-detector/back-end/data-test/v5/input-new/259.jpg"
imagePath8 = "traffic-sign-detector/back-end/data-test/v5/input-new/264.jpg"
imagePath = imagePath8


mode = sys.argv[1]
imagePath = sys.argv[2]


response = DP.mainProcess(imagePath, mode)

if mode == "web-detect":
    print(json.dumps(response))

# try:
#     model = torch.hub.load('dataset-yolov5/traffic-project1/yolov5', 'custom', 'dataset-yolov5/traffic-project1/yolov5/runs/train/exp/weights/best.pt', source='local', force_reload=True)
# except Exception as e:
#     print("Error loading model: ", e)
#     sys.exit(1)

# response1 = {
#     "text": [
#         {"number": 1,"main_text": "hello", "id": 69},
#         {"number": 2,"main_text": "dg1235", "id": 1412}
#         ]
#     }
# try:
#     print(json.dumps(response1, ensure_ascii=False).encode('utf-8'))
# except Exception as e:
#     print("Error encoding response1 as JSON: ", e)
#     sys.exit(1)


# print(DL.calAccuracy(0, 0, 0, 0))
# x = DL.checkShape('a', 'a')
# print(x)

# x = imagePath2.split("/")[-1].split(".")[0]
# print(x)
# print(x.isdigit())

# subObject = {
#         "number": 12,
#         "type": "one",
#         "shape": "circle",
#         "color": "red",
#         "state": "use"
# }
# print(subObject["state"])
# subObject["state"] = "no"
# print(subObject["state"])