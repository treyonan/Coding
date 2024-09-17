// Executor function, resolve(), reject()

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


// The Node setTimeout() Function

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