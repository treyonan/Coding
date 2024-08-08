function sayThanks(name) {
  console.log('Thank you for your purchase ' + name + '! We appreciate your business.');
}

sayThanks('Cole');

// Default parameters

function greeting(name = 'stranger') {
  console.log(`Hello, ${name}!`)
}

greeting('Nick') // Output: Hello, Nick!
greeting() // Output: Hello, stranger!

// Return values

function monitorCount(rows, columns) {
  return rows * columns;
}

const numOfMonitors = monitorCount(5, 4);

console.log(numOfMonitors);

//------------------------------------------------

function monitorCount(rows, columns) {
  return rows * columns;
}

function costOfMonitors(rows, columns) {
  return monitorCount(rows, columns) * 200;
}

const totalCost = costOfMonitors(5, 4);

console.log(totalCost);

// Function Expressions

const plantNeedsWater = function (day) {
  if (day === 'Wednesday') {
    return true;
  } else {
    return false;
  }
};

console.log(plantNeedsWater('Tuesday'));

// Arrow Functions

const plantNeedsWater = (day) => {
  if (day === 'Wednesday') {
    return true;
  } else {
    return false;
  }
};

// Concise Body Arrow Functions

const plantNeedsWater = day => day === 'Wednesday' ? true : false;


// Rock, Paper or Scissors Project

console.log('hi');

const getUserChoice = userInput => {
  userInput = userInput.toLowerCase();
  if (userInput === 'rock' || userInput === 'paper' || userInput === 'scissors' || userInput === 'bomb') {
    return userInput
  } else {
    console.log('Error message');
  }
}

function getComputerChoice() {
  num = Math.floor(Math.random() * 3);
  if (num === 0) {
    return 'rock';
  } else if (num === 1) {
    return 'paper';
  } else if (num === 2) {
    return 'scissors';
  }
}

function determineWinner(userChoice, computerChoice) {
  if (userChoice === computerChoice) {
    return 'Tie game';
  }
  if (userChoice === 'rock') {
    if (computerChoice === 'paper') {
      return 'computer won';
    } else {
      return 'user won';
    }
  }
  if (userChoice === 'paper') {
    if (computerChoice === 'scissors') {
      return 'computer won';
    } else {
      return 'user won';
    }
  }
  if (userChoice === 'scissors') {
    if (computerChoice === 'rock') {
      return 'computer won';
    } else {
      return 'user won';
    }
  }
  if (userChoice === 'bomb') {
    return 'user won';
  }
}

function playGame() {
  let userChoice = getUserChoice('paper');
  let computerChoice = getComputerChoice();
  console.log(determineWinner(userChoice, computerChoice));
}

playGame();


// Sleep Debt Project

function getSleepHours(day) {
  if (day === 'monday') {
    return 7;
  } else if (day === 'tuesday') {
    return 8;
  } else if (day === 'wednesday') {
    return 8;
  } else if (day === 'thursday') {
    return 6;
  } else if (day === 'friday') {
    return 8;
  } else if (day === 'saturday') {
    return 8;
  } else if (day === 'sunday') {
    return 8;
  } else {
    return 0;
  }
}

function getActualSleepHours() {
  let actualSleepHours = getSleepHours('monday') + getSleepHours('tuesday') + getSleepHours('wednesday') + getSleepHours('thursday') + getSleepHours('friday') + getSleepHours('saturday') + getSleepHours('sunday');
  return actualSleepHours;
}

function getIdealSleepHours() {
  let idealSleepHours = 8;
  return idealSleepHours * 7;
}

function calculateSleepDebt() {
  let actualSleepHours = getActualSleepHours();
  let idealSleepHours = getIdealSleepHours();
  if (actualSleepHours === idealSleepHours) {
    console.log('perfect amount of sleep');
  } else if (actualSleepHours < idealSleepHours) {
    console.log(`you need ${idealSleepHours - actualSleepHours} more hours of rest`);
  } else if (actualSleepHours > idealSleepHours) {
    console.log(`you slept ${actualSleepHours - idealSleepHours} more hours than needed`); 
  }
}

calculateSleepDebt();