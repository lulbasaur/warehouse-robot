const WebSocket = require("ws");
const util = require("util");
const cv = require("opencv");
const express = require("express");

const width = 620;
const height = 440;
const fps = 20;

const camera = new cv.VideoCapture(0);
camera.setWidth(width);
camera.setHeight(height);

const wss = new WebSocket.Server({
  port: 8080
});

const broadcast = data =>
  wss.clients.forEach(client => {
    if ((client.readyState = WebSocket.OPEN)) {
      client.send(data);
    }
  });

const delay = 20;
const sendFrame = () =>
  camera.read((err, image) => {

    broadcast(image.toBuffer());

  });

setInterval(() => {
  sendFrame();
}, 1000 / fps);


express().use(express.static('static')).listen(8081)