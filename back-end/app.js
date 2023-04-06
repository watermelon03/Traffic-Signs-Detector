const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const { PythonShell } = require("python-shell");
const multer = require("multer");
const fs = require("fs");
const NodeCache = require("node-cache");

const app = express();

let PORT = process.env.PORT || 5000

const storage = multer.diskStorage({
    destination: function (req, file, cb) {
      cb(null, "uploads/")
    },
    filename: function (req, file, cb) {
      cb(null, file.fieldname + "-" + Date.now())
    }
  });
const upload = multer({ storage: storage });

app.use(cors({
    origin: "*",
}));
app.use((req, res, next) => {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Methods", "GET, POST");
    res.header("Access-Control-Allow-Headers", "Origin, X-requested-With, Content-Type, Accept");
    next();
});
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const cache = new NodeCache();
const objectBaseAccuracy = {
    avgAccuracyType: 0.735,
    avgAccuracyShape: 0.738,
    avgAccuracyColor: 0.849,
    imageDetected: 226,
    imageTotal: 244,
}
cache.set("keyAcc", objectBaseAccuracy)

app.get("/", (req, res) => {
    console.log("Server working method GET path /");
    const nameUser = req.body.name
    res.send("Hello, Welcome to my server. " + nameUser);
});

app.get("/testGetAccuracy", (req, res) => {
    console.log("Server working method GET path /testGetAccuracy");
    const objectAcc = cache.get("keyAcc")
    res.json(objectAcc);
});

app.get('/testGetImage', (req, res) => {
    console.log("Server working method GET path /testGetImage");
    const image = fs.readFileSync('image/00105.jpg');
    const imageBuffer = new Buffer.from(image).toString('base64');
    // res.set('Content-Type', 'image/jpeg');
    res.json(
        {
            state: true,
            image: imageBuffer,
            text: "I love you so much"
        });
    // res.send(imageBuffer);
});

app.post("/testPostText", (req, res) => {
    console.log("Server working method POST path /testPostText");
    const getData1 = req.body.input;
    const getData2 = req.body.name;
    res.json(
        {
            message: "Data received successfully",
            data1: getData1,
            data2: getData2
        });
});

app.post("/testPostImageModel",upload.single('image'), async (req, res) => {
    console.log("Server working method POST path /testPostImageModel");
    const {text} = req.body;
    const {path:image} = req.file;
    const model = await modelMain
    try{
        const pythonScript = "grayFunction.py";
        const option = {
            mode: "text",
            pythonPath: "C:/Users/Watermelon/AppData/Local/Microsoft/WindowsApps/PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0/python.exe",
            pythonOptions: ["-u"],
            scriptPath: "./",
            args: [text, image, JSON.stringify(model)]
        };
        PythonShell.run(pythonScript, option, function (error, results){
            if(error) throw error;
            const result = JSON.parse(results[0]);
            const newText = result.text;
            const imagePath = result.image_path;

            const image = fs.readFileSync(imagePath);
            const imageBuffer = new Buffer.from(image).toString('base64');

            res.json(
                {
                    state: true,
                    text: newText,
                    image: imageBuffer,
                });
            // res.send(result);
        });
    }catch(error){
        res.status(500).send(error);
    }
});

app.post("/testPostImage",upload.single('image'), async (req, res) => {
    console.log("Server working method POST path /testPostImage");
    const {text} = req.body;
    const {path:image} = req.file;
    try{
        const pythonScript = "grayFunction.py";
        const option = {
            mode: "text",
            pythonPath: "C:/Users/Watermelon/AppData/Local/Microsoft/WindowsApps/PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0/python.exe",
            pythonOptions: ["-u"],
            scriptPath: "./",
            args: [text, image]
        };
        PythonShell.run(pythonScript, option, function (error, results){
            if(error) throw error;
            const result = JSON.parse(results[0]);
            const newText = result.text;
            const imagePath = result.image_path;

            const image = fs.readFileSync(imagePath);
            const imageBuffer = new Buffer.from(image).toString('base64');

            res.json(
                {
                    state: true,
                    text: newText,
                    image: imageBuffer,
                });
            // res.send(result);
        });
    }catch(error){
        res.status(500).send(error);
    }
});

app.post("/testPostDetector",upload.single('image'), async (req, res) => {
    console.log("Server working method POST path /testPostDetector");
    const {text} = req.body;
    const {path:image} = req.file;
    // const signal = req.signal;
    // let model = cache.get('modelKey');
    // console.log(model)
    try{
        const pythonScript = "detector.py";
        const option = {
            mode: "text",
            pythonPath: "C:/Users/Watermelon/AppData/Local/Microsoft/WindowsApps/PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0/python.exe",
            pythonOptions: ["-u"],
            scriptPath: "./",
            args: [text, image]
        };
        PythonShell.run(pythonScript, option, function (error, results){
            // console.log(results);
            if(error) throw error;
            let index = 0
            let resultsOne = results[index].toString()
            // console.log(typeof resultsOne);
            while(resultsOne.includes("'charmap'")){
                console.log("Error: ",resultsOne);
                index = index + 1;
                resultsOne = results[index].toString()
                if(index > 10){
                    break;
                }
            }
            const result = JSON.parse(results[index]);
            // const result = JSON.parse(results[1].toString('utf-8'));
            const state = result.state;
            const imagePath = result.imagePath;
            const objectInfo = result.objectInfo;
            const accuracy = result.accuracy;

            const image = fs.readFileSync(imagePath);
            const imageBuffer = new Buffer.from(image).toString('base64');

            res.json(
                {
                    state: state,
                    imagePath: imageBuffer,
                    objectInfo: objectInfo,
                    accuracy: accuracy
                });
        });
    }catch(error){
        res.status(500).send(error);
    }
});

app.post("/testPostVideo",upload.single('video'), async (req, res) => {
    console.log("Server working method POST path /testPostVideo");
    const {text} = req.body;
    const {path:video} = req.file;
    try{
        const pythonScript = "detectorVideo.py";
        const option = {
            mode: "text",
            pythonPath: "C:/Users/Watermelon/AppData/Local/Microsoft/WindowsApps/PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0/python.exe",
            pythonOptions: ["-u"],
            scriptPath: "./",
            args: [text, video]
        };
        PythonShell.run(pythonScript, option, function (error, results){
            // console.log(results);
            if(error) throw error;
            let index = 0
            let resultsOne = results[index].toString()
            // console.log(typeof resultsOne);
            while(resultsOne.includes("'charmap'")){
                console.log("Error: ",resultsOne);
                index = index + 1;
                resultsOne = results[index].toString()
                if(index > 10){
                    break;
                }
            }
            const result = JSON.parse(results[index]);
            const state = result.state;
            const typePath = result.typePath;
            const shapePath = result.shapePath

            const type = fs.readFileSync(typePath);
            const typeBuffer = new Buffer.from(type).toString('base64');

            const shape = fs.readFileSync(shapePath);
            const shapeBuffer = new Buffer.from(shape).toString('base64');

            res.json(
                {
                    state: state,
                    typePath: typeBuffer,
                });
        });
    }catch(error){
        res.status(500).send(error);
    }
});

app.post("/testPostAccuracy",upload.single('image'), async (req, res) => {
    console.log("Server working method POST path /testPostAccuracy");
    const {text} = req.body;
    try{
        const pythonScript = "detectorAccuracy.py";
        const option = {
            mode: "text",
            pythonPath: "C:/Users/Watermelon/AppData/Local/Microsoft/WindowsApps/PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0/python.exe",
            pythonOptions: ["-u"],
            scriptPath: "./",
            args: [text]
        };
        PythonShell.run(pythonScript, option, function (error, results){
            if(error) throw error;
            let index = 0
            let resultsOne = results[index].toString()
            // console.log(typeof resultsOne);
            while(resultsOne.includes("'charmap'")){
                console.log("Error: ",resultsOne);
                index = index + 1;
                resultsOne = results[index].toString()
                if(index > 10){
                    break;
                }
            }
            const result = JSON.parse(results[index]);

            const accShape = result.shape;
            const accColor = result.color;
            const accType = result.type;
            const total = result.countTotal
            const detected = result.countDetect

            let objecctAcc = {
                avgAccuracyType: accType,
                avgAccuracyShape: accShape,
                avgAccuracyColor: accColor,
                imageDetected: detected,
                imageTotal: total,
            }
            cache.set("keyAcc", objecctAcc);

            res.json(objecctAcc);
            // res.send(result);
        });
    }catch(error){
        res.status(500).send(error);
    }
});

app.listen(PORT, () => {
    console.log("Server is running on port 5000");
});