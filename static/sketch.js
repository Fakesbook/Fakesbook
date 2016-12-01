var screenSize;
var number;
var circleSize;
var radius;

var lines = {};
var circleLocations = [];
var colorForCircle = {};

function setup() {
   circleSize = 400;
   number = 20;
   radius = 50;

   createCanvas(windowWidth - 50, windowHeight - 50);
   for(i = 0; i < number; i++) {
      lines[i] = [];
      colorForCircle[i] = [255, 255/number * i, 203];
   }
}

function windowResized() {
    resizeCanvas(windowWidth - 50, windowHeight - 50);
}

function convertX(ndx) {
   return windowWidth/2 + circleSize/2 * cos(ndx * TWO_PI/number);
}

function convertY(ndx) {
   return windowHeight/2 + circleSize/2 * sin(ndx * TWO_PI/number);
}

function draw() {
   for(i = 0; i < number; i++) {
      x = convertX(i);
      y = convertY(i)/2;
      circleLocations.push([x, y]);
      if (lines[i].length > 1) {
         colorForCircle[i] = [0, 255, 255];
      }
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
