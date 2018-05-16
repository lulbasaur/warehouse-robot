const WebSocket = require("ws");
const util = require("util");
var cv = require("opencv");

// camera properties
var width = 620;
var height = 440;
var fps = 10;

// face detection properties
var rectColor = [0, 255, 0];
var rectThickness = 2;

// initialize camera
var camera = new cv.VideoCapture(0);
camera.setWidth(width);
camera.setHeight(height);

camera.read(console.log);

const wss = new WebSocket.Server({ port: 8080 });

const broadcast = data =>
  wss.clients.forEach(client => {
    if ((client.readyState = WebSocket.OPEN)) {
      client.send(data);
    }
  });

const delay = 20;
const sendFrame = () =>
  camera.read((err, image) => {
    image.detectObject(cv.FACE_CASCADE, {}, (err, faces) => {
      for (var i = 0; i < faces.length; i++) {
        var x = faces[i];
        image.ellipse(
          x.x + x.width / 2,
          x.y + x.height / 2,
          x.width / 2,
          x.height / 2
        );
      }
      broadcast(image.toBuffer());
    });
  });

setInterval(() => {
  sendFrame();
}, 1000 / fps);
