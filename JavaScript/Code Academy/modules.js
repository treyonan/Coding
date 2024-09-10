

/* shape-area.js */
const PI = Math.PI;

// Define and export circleArea() and squareArea() below
function circleArea(radius) {
  return PI * (radius * radius);
}

module.exports.circleArea = circleArea;

module.exports.squareArea = function(length) {
  return length * length;
};



/* app.js */ 

const radius = 5;
const sideLength = 10;

// Option 1: import the entire shape-area.js module here.
const areas = require('./shape-area.js');
const areaFunctions = areas.squareArea(sideLength);

// Option 2: import circleArea and squareArea with object destructuring

const { circleArea, squareArea } = require("./shape-area.js")

// use the imported .circleArea() and .squareArea() methods here

const areaOfCircle = circleArea(radius);

const areaOfSquare = squareArea(sideLength);