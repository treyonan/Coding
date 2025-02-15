function withConstructor(num) {
    return new Promise((resolve, reject) => {
        if (num === 0) {
            resolve('zero');
        } else {
            resolve('not zero');
        }
    });
}

withConstructor(0)
    .then((resolveValue) => {
        console.log(` withConstructor(0) returned a promise which resolved to: ${resolveValue}.`);
    });

// Write your code below:
async function withAsync(num) {
    if (num === 0) {
        return 'zero';
    } else {
        return 'not zero';
    }
}

withAsync(100)
    .then((resolveValue) => {
        console.log(` withAsync(100) returned a promise which resolved to: ${resolveValue}.`);
    });

// ------------------------------------------------------------------------

const fs = require('fs');
const promisifiedReadfile = require('./promisifiedReadfile');

// Here we use fs.readfile() and callback functions:
fs.readFile('./file.txt', 'utf-8', (err, data) => {
    if (err) throw err;
    let firstSentence = data;
    fs.readFile('./file2.txt', 'utf-8', (err, data) => {
        if (err) throw err;
        let secondSentence = data;
        console.log(firstSentence, secondSentence);
    });
});

// Here we use native promises with our "promisified" version of readfile:
let firstSentence;
promisifiedReadfile('./file.txt', 'utf-8')
    .then((data) => {
        firstSentence = data;
        return promisifiedReadfile('./file2.txt', 'utf-8');
    })
    .then((data) => {
        let secondSentence = data;
        console.log(firstSentence, secondSentence)
    })
    .catch((err) => { console.log(err) });

// Here we use promisifiedReadfile() again but instead of using the native promise .then() syntax, we declare and invoke an async/await function:
async function readFiles() {
    let firstSentence = await promisifiedReadfile('./file.txt', 'utf-8');
    let secondSentence = await promisifiedReadfile('./file2.txt', 'utf-8');
    console.log(firstSentence, secondSentence);
}

readFiles();
