const city = 'New York City';

function logCitySkyline() {
    let skyscraper = 'Empire State Building';
    return 'The stars over the ' + skyscraper + ' in ' + city;
}

console.log(logCitySkyline());


// Global variables

const satellite = 'The Moon';
const galaxy = 'The Milky Way';
const stars = 'North Star';

const callMyNightSky = () => {
    return 'Night Sky: ' + satellite + ', ' + stars + ', and ' + galaxy;
};

console.log(callMyNightSky());

// Block Scope

const logVisibleLightWaves = () => {
    const lightWaves = 'Moonlight';
    console.log(lightWaves);
};

logVisibleLightWaves();

console.log(lightWaves); // Throws error

// Scope Pollution

const satellite = 'The Moon';
const galaxy = 'The Milky Way';
let stars = 'North Star';

const callMyNightSky = () => {
    stars = 'Sirius';
    return 'Night Sky: ' + satellite + ', ' + stars + ', ' + galaxy;
};

console.log(callMyNightSky());
console.log(stars);

// Practice Good Scoping

const logSkyColor = () => {
    const dusk = true;
    let color = 'blue';
    if (dusk) {
        let color = 'pink';
        console.log(color); // Prints "pink"
    }
    console.log(color); // Prints "blue"
};

console.log(color); // throws a ReferenceError

const logVisibleLightWaves = () => {
    let lightWaves = 'Moonlight';
    let region = 'The Arctic';
    if (region === 'The Arctic') {
        let lightWaves = 'Northern Lights';
        console.log(lightWaves);
    }

    console.log(lightWaves);
};

logVisibleLightWaves();

// Training Days Project

const getRandEvent = () => {
    const random = Math.floor(Math.random() * 3);
    if (random === 0) {
      return "Marathon";
    } else if (random === 1) {
      return "Triathlon";
    } else if (random === 2) {
      return "Pentathlon";
    }
  };
  
  const getTrainingDays = (event) => {
    var days;
    if (event === "Marathon") {
      days = 50;
    } else if (event === "Triathlon") {
      days = 100;
    } else if (event === "Pentathlon") {
      days = 200;
    }
  
    return days;
  };
  
  const name = 'Trey';
  
  const logEvent = (name, event) => {  
    console.log(`${name}'s event is: ${event}`);
  };
  
  const logTime = (name, days) => {  
    console.log(`${name}'s time to train is: ${days} days`);
  };
  
  const event = getRandEvent();
  const days = getTrainingDays(event);
  
  logEvent(name, event);
  logTime(name, days);
  
  const event2 = getRandEvent();
  const days2 = getTrainingDays(event2);
  const name2 = 'Warren';
  
  logEvent(name2, event2);
  logTime(name2, days2);
  