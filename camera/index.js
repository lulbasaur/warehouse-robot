const WebSocket = require("ws");
const util = require("util");
const cv = require("opencv");

const width = 620;
const height = 440;
const fps = 10;

const camera = new cv.VideoCapture(0);
camera.setWidth(width);
camera.setHeight(height);

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
        let x = faces[i];
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
