// Executor function, resolve(), reject() -------------------------------------

const executorFunction = (resolve, reject) => {
    if (someCondition) {
        resolve('I resolved!');
    } else {
        reject('I rejected!');
    }
}
const myFirstPromise = new Promise(executorFunction);


   onst inventory = {
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
