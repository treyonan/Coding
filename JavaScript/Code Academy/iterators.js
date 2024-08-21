// .forEach(), .map(), .filter()

const artists = ['Picasso', 'Kahlo', 'Matisse', 'Utamaro'];

artists.forEach(artist => {
  console.log(artist + ' is one of my favorite artists.');
});

const numbers = [1, 2, 3, 4, 5];

const squareNumbers = numbers.map(number => {
  return number * number;
});

console.log(squareNumbers);

const things = ['desk', 'chair', 5, 'backpack', 3.14, 100];

const onlyNumbers = things.filter(thing => {
  return typeof thing === 'number';
});

console.log(onlyNumbers);

// .forEach()

const fruits = ['mango', 'papaya', 'pineapple', 'apple'];

fruits.forEach(item => console.log('I want to eat a ' + item));

// .map()

const animals = ['Hen', 'elephant', 'llama', 'leopard', 'ostrich', 'Whale', 'octopus', 'rabbit', 'lion', 'dog'];

const secretMessage = animals.map(item => item[0]);

console.log(secretMessage.join(''));

const bigNumbers = [100, 200, 300, 400, 500];

const smallNumbers = bigNumbers.map(item => item / 100);

// .filter()

const randomNumbers = [375, 200, 3.14, 7, 13, 852];

const smallNumbers = randomNumbers.filter(item => item < 250);

const favoriteWords = ['nostalgia', 'hyperbole', 'fervent', 'esoteric', 'serene'];

const longFavoriteWords = favoriteWords.filter(item => item.length > 7);

// .findIndex()

const animals = ['hippo', 'tiger', 'lion', 'seal', 'cheetah', 'monkey', 'salamander', 'elephant'];

const foundAnimal = animals.findIndex(item => item === 'elephant');

const startsWithS = animals.findIndex(item => item[0] === 's');

// .reduce()

const newNumbers = [1, 3, 5, 7];

const newSum = newNumbers.reduce((accumulator, currentValue) => {
  console.log('The value of accumulator: ', accumulator);
  console.log('The value of currentValue: ', currentValue);
  return accumulator + currentValue;
}, 10);

console.log(newSum);

// .some(), .every()

const words = ['unique', 'uncanny', 'pique', 'oxymoron', 'guise'];

console.log(words.some(word => {
  return word.length < 6;
}));

const interestingWords = words.filter((word) => {return word.length > 5});

console.log(interestingWords.every((word) => {return word.length > 5}));


const cities = ['Orlando', 'Dubai', 'Edinburgh', 'Chennai', 'Accra', 'Denver', 'Eskisehir', 'Medellin', 'Yokohama'];

const nums = [1, 50, 75, 200, 350, 525, 1000];

cities.forEach(city => console.log('Have you visited ' + city + '?'));

const longCities = cities.filter(city => city.length > 7);

const word = cities.reduce((acc, currVal) => {
  return acc + currVal[0]
}, "C");

console.log(word)

const smallerNums = nums.map(num => num - 5);

nums.some(num => num < 0);