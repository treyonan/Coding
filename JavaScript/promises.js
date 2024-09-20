// Executor function, resolve(), reject() -------------------------------------

const executorFunction = (resolve, reject) => {
    if (someCondition) {
        resolve('I resolved!');
    } else {
        reject('I rejected!');
    }
}
const myFirstPromise = new Promise(executorFunction);


const inventory = {
    sunglasses: 1900,
    pants: 1088,
    bags: 1344
};

const myExecutor = (resolve, reject) => {
    if (inventory.sunglasses > 0) {
        resolve('Sunglasses order processed.');
    } else {
        reject('That item is sold out.');
    }
};

const orderSunglasses = () => {
    return new Promise(myExecutor);
};

const orderPromise = orderSunglasses();

console.log(orderPromise);


// The Node setTimeout() Function ----------------------------------

// Example #1
const delayedHello = () => {
    console.log('Hi! This is an asynchronous greeting!');
};

setTimeout(delayedHello, 2000);

// Example #2
const returnPromiseFunction = () => {
    return new Promise((resolve, reject) => {
        setTimeout(() => { resolve('I resolved!') }, 1000);
    });
};

const prom = returnPromiseFunction();

//Example #3
console.log("This is the first line of code in app.js.");

const usingSTO = () => {
    console.log('Hello World');
}
setTimeout(usingSTO, 2000);

console.log("This is the last line of code in app.js.");

// Success and Failure Callback Functions --------------------------------

// Example #1
const prom = new Promise((resolve, reject) => {
    resolve('Yay!');
});

const handleSuccess = (resolvedValue) => {
    console.log(resolvedValue);
};

prom.then(handleSuccess); // Prints: 'Yay!'

// Example #2

let prom = new Promise((resolve, reject) => {
    let num = Math.random();
    if (num < .5) {
        resolve('Yay!');
    } else {
        reject('Ohhh noooo!');
    }
});

const handleSuccess = (resolvedValue) => {
    console.log(resolvedValue);
};

const handleFailure = (rejectionReason) => {
    console.log(rejectionReason);
};

prom.then(handleSuccess, handleFailure);

// Example #3

const inventory = {
    sunglasses: 1900,
    pants: 1088,
    bags: 1344
};

const checkInventory = (order) => {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            let inStock = order.every(item => inventory[item[0]] >= item[1]);
            if (inStock) {
                resolve(`Thank you. Your order was successful.`);
            } else {
                reject(`We're sorry. Your order could not be completed because some items are sold out.`);
            }
        }, 1000);
    })
};

module.exports = { checkInventory };

const { checkInventory } = require('./library.js');

const order = [['sunglasses', 1], ['bags', 2]];


const handleSuccess = (resolvedValue) => {
    console.log(resolvedValue);
};

const handleFailure = (rejectReason) => {
    console.log(rejectReason);
};

checkInventory(order)
    .then(handleSuccess, handleFailure);


// Using catch() with Promises

prom
    .then((resolvedValue) => {
        console.log(resolvedValue);
    })
    .then(null, (rejectionReason) => {
        console.log(rejectionReason);
    });

prom
    .then((resolvedValue) => {
        console.log(resolvedValue);
    })
    .catch((rejectionReason) => {
        console.log(rejectionReason);
    });

const { checkInventory } = require('./library.js');

const order = [['sunglasses', 1], ['bags', 2]];

const handleSuccess = (resolvedValue) => {
    console.log(resolvedValue);
};

const handleFailure = (rejectReason) => {
    console.log(rejectReason);
};

// Write your code below:
checkInventory(order).then(handleSuccess).catch(handleFailure);


// Chaining Multiple Promises -------------------------------------

firstPromiseFunction()
    .then((firstResolveVal) => {
        return secondPromiseFunction(firstResolveVal);
    })
    .then((secondResolveVal) => {
        console.log(secondResolveVal);
    });

// Example for order tracking, processing and shipping

const store = {
    sunglasses: {
        inventory: 817,
        cost: 9.99
    },
    pants: {
        inventory: 236,
        cost: 7.99
    },
    bags: {
        inventory: 17,
        cost: 12.99
    }
};

const checkInventory = (order) => {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            const itemsArr = order.items;
            let inStock = itemsArr.every(item => store[item[0]].inventory >= item[1]);

            if (inStock) {
                let total = 0;
                itemsArr.forEach(item => {
                    total += item[1] * store[item[0]].cost
                });
                console.log(`All of the items are in stock. The total cost of the order is ${total}.`);
                resolve([order, total]);
            } else {
                reject(`The order could not be completed because some items are sold out.`);
            }
        }, generateRandomDelay());
    });
};

const processPayment = (responseArray) => {
    const order = responseArray[0];
    const total = responseArray[1];
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            let hasEnoughMoney = order.giftcardBalance >= total;
            // For simplicity we've omited a lot of functionality
            // If we were making more realistic code, we would want to update the giftcardBalance and the inventory
            if (hasEnoughMoney) {
                console.log(`Payment processed with giftcard. Generating shipping label.`);
                let trackingNum = generateTrackingNumber();
                resolve([order, trackingNum]);
            } else {
                reject(`Cannot process order: giftcard balance was insufficient.`);
            }

        }, generateRandomDelay());
    });
};


const shipOrder = (responseArray) => {
    const order = responseArray[0];
    const trackingNum = responseArray[1];
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve(`The order has been shipped. The tracking number is: ${trackingNum}.`);
        }, generateRandomDelay());
    });
};


// This function generates a random number to serve as a "tracking number" on the shipping label. In real life this wouldn't be a random number
function generateTrackingNumber() {
    return Math.floor(Math.random() * 1000000);
}

// This function generates a random number to serve as delay in a setTimeout() since real asynchrnous operations take variable amounts of time
function generateRandomDelay() {
    return Math.floor(Math.random() * 2000);
}

module.exports = { checkInventory, processPayment, shipOrder };



const { checkInventory, processPayment, shipOrder } = require('./library.js');

const order = {
    items: [['sunglasses', 1], ['bags', 2]],
    giftcardBalance: 79.82
};

checkInventory(order)
    .then((resolvedValueArray) => {
        return processPayment(resolvedValueArray);

    })
    .then((resolvedValueArray) => {
        return shipOrder(resolvedValueArray);

    })
    .then((successMessage) => {
        console.log(successMessage);
    })
    .catch((errorMessage) => {
        console.log(errorMessage);
    });


// Using Promise.all() ---------------------------------------------------------

let myPromises = Promise.all([returnsPromOne(), returnsPromTwo(), returnsPromThree()]);

myPromises
    .then((arrayOfValues) => {
        console.log(arrayOfValues);
    })
    .catch((rejectionReason) => {
        console.log(rejectionReason);
    });

// Check availability example

const checkAvailability = (itemName, distributorName) => {
    console.log(`Checking availability of ${itemName} at ${distributorName}...`);
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (restockSuccess()) {
                console.log(`${itemName} are in stock at ${distributorName}`)
                resolve(itemName);
            } else {
                reject(`Error: ${itemName} is unavailable from ${distributorName} at this time.`);
            }
        }, 1000);
    });
};

module.exports = { checkAvailability };


// This is a function that returns true 80% of the time
// We're using it to simulate a request to the distributor being successful this often
function restockSuccess() {
    return (Math.random() > .2);
}

const { checkAvailability } = require('./library.js');

const onFulfill = (itemsArray) => {
    console.log(`Items checked: ${itemsArray}`);
    console.log(`Every item was available from the distributor. Placing order now.`);
};

const onReject = (rejectionReason) => {
    console.log(rejectionReason);
};

const checkSunglasses = checkAvailability('sunglasses', 'Favorite Supply Co.');
const checkPants = checkAvailability('pants', 'Favorite Supply Co.');
const checkBags = checkAvailability('bags', 'Favorite Supply Co.');

Promise.all([checkSunglasses, checkPants, checkBags])
    .then(onFulfill)
    .catch(onReject);



