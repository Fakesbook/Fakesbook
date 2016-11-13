var screenSize;
var number;
var circleSize;
var radius

var dictionary = {};
var circleLocations = [];
var colorForCircle = {};
var img;

function preload(){
   img = loadImage("/static/puppy.jpg");
}

function setup() {
   screenSize = 600;
   circleSize = 400;
   number = 20;
   radius = 50;

   createCanvas(screenSize, screenSize);
   for(i = 0; i < number; i++) {
      dictionary[i] = [];
      colorForCircle[i] = [255, 255/number * i, 203];
   }
}

function convertX(ndx) {
   return screenSize/2 + circleSize/2 * cos(ndx * TWO_PI/number);
}

function convertY(ndx) {
   return screenSize/2 + circleSize/2 * sin(ndx * TWO_PI/number);
}

function addLine(ndx1, ndx2) {
   dictionary[ndx1].push(ndx2);
   dictionary[ndx2].push(ndx1);
   x1 = convertX(ndx1);
   y1 = convertY(ndx1);
   x2 = convertX(ndx2);
   y2 = convertY(ndx2);
   line(x1, y1, x2, y2);
}

function draw() {
   addLine(0, 5);
   addLine(0, 10);
   addLine(1, 8);
   for(i = 0; i < number; i++) {
      if (dictionary[i].length > 1) {
         colorForCircle[i] = [0, 255, 255];
      }
      x = convertX(i);
      y = convertY(i);
      circleLocations.push([x, y]);
      fill(colorForCircle[i][0], colorForCircle[i][1], colorForCircle[i][2]);
      ellipse(x,y, radius, radius);
   } 
}

function mouseClicked() {
   for (i = 0; i < circleLocations.length; i++) {
      if(dist(mouseX, mouseY, circleLocations[i][0], circleLocations[i][1]) < radius/2) {
         colorForCircle[i] = [255/number * i, 0, 255];
      }
   }
}
