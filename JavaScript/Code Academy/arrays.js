let newYearsResolutions = ['Keep a journal', 'Take a falconry class', 'Learn to juggle'];

console.log(newYearsResolutions);

let groceryList = ['bread', 'tomatoes', 'milk'];
groceryList[1] = 'avocados';


// const and let arrays

let condiments = ['Ketchup', 'Mustard', 'Soy Sauce', 'Sriracha'];

const utensils = ['Fork', 'Knife', 'Chopsticks', 'Spork'];

condiments[0] = 'Mayo';

console.log(condiments);

condiments = ['Mayo'];

console.log(condiments);

utensils[3] = 'Spoon';

console.log(utensils);

// Length

const objectives = ['Learn a new language', 'Read 52 books', 'Run a marathon'];

console.log(objectives.length);

// Push adds elements at the end of array

const chores = ['wash dishes', 'do laundry', 'take out trash'];

chores.push('read', 'homework');

console.log(chores);

// Pop removes the last item in array

const chores = ['wash dishes', 'do laundry', 'take out trash', 'cook dinner', 'mop floor'];

chores.pop();

console.log(chores);

// Shift deletes element to the front

const groceryList = ['orange juice', 'bananas', 'coffee beans', 'brown rice', 'pasta', 'coconut oil', 'plantains'];

groceryList.shift();
console.log(groceryList);

// Unshift adds elements to the front

groceryList.unshift('popcorn');
console.log(groceryList);

// Slice returns a subset

groceryList.slice(1, 4);
console.log(groceryList);


// indexOf finds the index of a specific item

const pastaIndex = groceryList.indexOf('pasta');

console.log(pastaIndex);

// Arrays and Functions
 
const concept = ['arrays', 'can', 'be', 'mutated'];

function changeArr(arr){
  arr[3] = 'MUTATED';
}

changeArr(concept);

console.log(concept);

const removeElement = newArr => {
  newArr.pop()
}

removeElement(concept);

console.log(concept);

// Nested Arrays

const numberClusters = [[1, 2], [3, 4], [5, 6]];

const target = numberClusters[2][1];

// Secret Message Project

let secretMessage = ['Learning', 'is', 'not', 'about', 'what', 'you', 'get', 'easily', 'the', 'first', 'time,', 'it', 'is', 'about', 'what', 'you', 'can', 'figure', 'out.', '-2015,', 'Chris', 'Pine,', 'Learn', 'JavaScript'];

secretMessage.pop(); // remove last element
console.log(secretMessage);
console.log(secretMessage.length); // print length
secretMessage[7] = 'right'; // replace element 7 with 'right'
console.log(secretMessage);
secretMessage.shift(); // remove first element
console.log(secretMessage);
secretMessage.unshift('Programming'); // Add programming to front
console.log(secretMessage);
let startIndex = secretMessage.indexOf('get');
secretMessage.splice(startIndex, 5, 'know,');
console.log(secretMessage);
console.log(secretMessage.join(' '));
