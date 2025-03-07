console.log(5);

// single line comment
/*
multi line comment
*/

console.log(11 % 3);
console.log('hiyah'.length);

console.log('Hello' + 'World');

console.log('Codecademy'.toUpperCase());
console.log('    Remove whitespace   '.trim());

console.log(Math.floor(Math.random() * 100));
console.log(Math.ceil(43.8));
console.log(Number.isInteger(2017));

let levelUp = 10;
let powerLevel = 9001;
let multiplyMe = 32;
let quarterMe = 1152;

// Use the mathematical assignments in the space below:
levelUp += 5;
powerLevel -= 100;
multiplyMe *= 11;
quarterMe /= 4;

// These console.log() statements below will help you check the values of the variables.
// You do not need to edit these statements. 
console.log('The value of levelUp:', levelUp); 
console.log('The value of powerLevel:', powerLevel); 
console.log('The value of multiplyMe:', multiplyMe); 
console.log('The value of quarterMe:', quarterMe);

let gainedDollar = 3;
let lostDollar = 50;
gainedDollar ++;
lostDollar --;

var myName = 'Trey';
var myCity = 'OKC';
console.log(`My name is ${myName}. My favorite city is ${myCity}`);

let newVariable = 'Playing around with typeof.';
console.log(typeof newVariable);
newVariable = 1;
console.log(typeof newVariable);

// constant for kelvin
const kelvin = 50;
// constant for celsius is kelvin minus 273
const celsius = kelvin - 273;
// fahrenheit
const fahrenheit = Math.floor(celsius * (9/5) + 32);

console.log(`The temperature is ${fahrenheit} degrees Fahrenheit`);

//ternary operator

let isLocked = false;

isLocked ? console.log('You will need a key to open the door.')
: console.log('You will not need a key to open the door.')


let isCorrect = true;

isCorrect ? console.log('Correct!')
: console.log('Incorrect!')


let favoritePhrase = 'Love That!';

favoritePhrase === 'Love That!' ? console.log('I love that!')
: console.log("I don't love that!")

// switch statements

let athleteFinalPosition = 'first place';

switch(athleteFinalPosition){
  case 'first place':
    console.log('You get the gold medal!');
    break;
  case 'second place':
    console.log('You get the silver medal!');
    break;
  case 'third place':
    console.log('You get the bronze medal!');
    break;
  default:
    console.log('No medal awarded.');
    break;
}

// Magic 8 Ball Project

let userName = 'Trey';
userName !== '' ? console.log(`Hello, ${userName}`) : console.log('Hello')
let userQuestion = 'Will I be rich someday?';
console.log(`${userName} asked ${userQuestion}`);
let randomNumber = Math.floor(Math.random() * 8);
let eightBall = '';
switch(randomNumber){
  case 0:
    eightBall = 'It is certain';
    break;
  case 1:
    eightBall = 'It is decidedly so';
    break;
  case 2:
    eightBall = 'Reply hazy try again';
    break;
  case 3:
    eightBall = 'Cannot predict now';
    break;
  case 4:
    eightBall = 'Do not count on it';
    break;
  case 5:
    eightBall = 'My sources say so';
    break;
  case 6:
    eightBall = 'Outlook not so good';
    break;
  case 7:
    eightBall = 'Signs point to yes';
    break;  
  default:
    eightBall = 'blah';
    break;
}
console.log(eightBall);

// Race Day Project

let raceNumber = Math.floor(Math.random() * 1000);
let registeredEarly = false;
let age = 18;
if (age > 18 && registeredEarly) {
  raceNumber += 1000;
}
if (age > 18 && registeredEarly) {
  console.log(`You will race at 9:30 am, your race number is ${raceNumber}`);
} else if (age > 18 && !registeredEarly) {
  console.log(`You will race at 11:00 am, your race number is ${raceNumber}`);
}
if (age < 18) {
  console.log(`You will race at 12:30 pm, your race number is ${raceNumber}`);
}
if (age === 18) {
  console.log(`See registration desk`);
}
