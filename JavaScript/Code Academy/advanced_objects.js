const robot = {
    model: 'B-4MI',
    mobile: true,
    greeting() {
        console.log(`I'm model ${this.model}, how may I be of service?`);
    }
}

const massProdRobot = (model, mobile) => {
    return {
        model,
        mobile,
        greeting() {
            console.log(`I'm model ${this.model}, how may I be of service?`);
        }
    }
}

const shinyNewRobot = massProdRobot('TrayHax', true)

const chargingStation = {
    _name: 'Electrons-R-Us',
    _robotCapacity: 120,
    _active: true,
    _chargingRooms: ['Low N Slow', 'Middle of the Road', 'In and Output'],

    set robotCapacity(newCapacity) {
        if (typeof newCapacity === 'number') {
            this._robotCapacity = newCapacity;
        } else {
            console.log(`Change ${newCapacity} to a number.`)
        }
    },
    get robotCapacity() {
        return this._robotCapacity;
    }
}

// The this keyword

const goat = {
    dietType: 'herbivore',
    makeSound() {
        console.log('baaa');
    },
    diet() {
        console.log(this.dietType);
    }
};

goat.diet();
// Output: herbivore

const robot = {
    model: '1E78V2',
    energyLevel: 100,
    provideInfo() {
        return `I am ${this.model} and my current energy level is ${this.energyLevel}.`
    }
};

console.log(robot.provideInfo());


// Privacy

const robot = {
    _energyLevel: 100,
    recharge() {
        this._energyLevel += 30;
        console.log(`Recharged! Energy is currently at ${this._energyLevel}%.`)
    }
};

robot._energyLevel = 'high';
robot.recharge();


// Getters

const robot = {
    _model: '1E78V2',
    _energyLevel: 100,
    get energyLevel() {
        if (typeof this._energyLevel === 'number') {
            return 'My current energy level is ' + this._energyLevel
        } else {
            return "System malfunction: cannot retrieve energy level"
        }
    }
};

console.log(robot.energyLevel);

// Setters

const robot = {
    _model: '1E78V2',
    _energyLevel: 100,
    _numOfSensors: 15,
    get numOfSensors() {
        if (typeof this._numOfSensors === 'number') {
            return this._numOfSensors;
        } else {
            return 'Sensors are currently down.'
        }
    },
    set numOfSensors(num) {
        if (typeof num === 'number' && num >= 0) {
            this._numOfSensors = num;
        } else {
            console.log('Pass in a number that is greater than or equal to 0')
        }
    }
};

robot.numOfSensors = 100;
console.log(robot.numOfSensors);


// Factory Functions

const monsterFactory = (name, age, energySource, catchPhrase) => {
    return {
        name: name,
        age: age,
        energySource: energySource,
        scare() {
            console.log(catchPhrase);
        }
    }
};


const robotFactory = (model, mobile) => {
    return {
        model: model,
        mobile: mobile,
        beep() {
            console.log('Beep Boop');
        }
    };
};

const tinCan = robotFactory('P-500', true);
tinCan.beep();

// Property Value Shorhand

const robotFactory = (model, mobile) => {
    return {
        model,
        mobile,
        beep() {
            console.log('Beep Boop');
        }
    }
}

// To check that the property value shorthand technique worked:
const newRobot = robotFactory('P-501', false)
console.log(newRobot.model)
console.log(newRobot.mobile)


// Destructured Assignment

const vampire = {
    name: 'Dracula',
    residence: 'Transylvania',
    preferences: {
        day: 'stay inside',
        night: 'satisfy appetite'
    }
};

const { residence } = vampire;
console.log(residence); // Prints 'Transylvania'

const { day } = vampire.preferences;
console.log(day); // Prints 'stay inside'


// Built-in Object Methods

const robot = {
    model: 'SAL-1000',
    mobile: true,
    sentient: false,
    armor: 'Steel-plated',
    energyLevel: 75
};

const robotKeys = Object.keys(robot);
console.log(robotKeys);

const robotEntries = Object.entries(robot)
console.log(robotEntries);

const newRobot = Object.assign({ laserBlaster: true, voiceRecognition: true }, robot);

console.log(newRobot);


// Meal Maker Project

const menu = {
    _meal: '',
    _price: 0,

    set meal(mealToCheck) {
        if (typeof mealToCheck === 'string') {
            return this._meal = mealToCheck;
        }
    },

    set price(priceToCheck) {
        if (typeof priceToCheck === 'number') {
            return this._price = priceToCheck;
        }
    },

    get todaySpecial() {
        if (this._meal && this._price) {
            return `Today's Meal is ${this._meal} for ${this._price}!`;
        } else {
            return `Meal or price not set correctly!`;
        }
    }
};

menu.meal = 'Pizza';
menu.price = 8;
console.log(menu.todaySpecial);

