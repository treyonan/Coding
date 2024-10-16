// Set variable to function

const checkThatTwoPlusTwoEqualsFourAMillionTimes = () => {
    for (let i = 1; i <= 1000000; i++) {
        if ((2 + 2) != 4) {
            console.log('Something has gone very wrong :( ');
        }
    }
};

const isTwoPlusTwo = checkThatTwoPlusTwoEqualsFourAMillionTimes;
isTwoPlusTwo();
console.log(isTwoPlusTwo.name);

// Functions as parameters. Callback Functions

const higherOrderFunc = param => {
    param();
    return `I just invoked ${param.name} as a callback function!`
}

const anotherFunc = () => {
    return 'I\'m being invoked by the higher-order function!';
}

higherOrderFunc(anotherFunc);


const addTwo = num => {
    return num + 2;
}

const checkConsistentOutput = (func, val) => {
    let checkA = val + 2;
    let checkB = func(val);
    if (checkA === checkB) {
        return checkB;
    } else {
        console.log('inconsistent results');
    }

}

console.log(checkConsistentOutput(addTwo, 4));

// Grammer Checker Project

let story = 'Last weekend, I took literally the most beautifull bike ride of my life. The route is called "The 9W to Nyack" and it stretches all the way from Riverside Park in Manhattan to South Nyack, New Jersey. It\'s really an adventure from beginning to end! It is a 48 mile loop and it literally took me an entire day. I stopped at Riverbank State Park to take some artsy photos. It was a short stop, though, because I had a freaking long way to go. After a quick photo op at the very popular Little Red Lighthouse I began my trek across the George Washington Bridge into New Jersey. The GW is a breathtaking 4,760 feet long! I was already very tired by the time I got to the other side. An hour later, I reached Greenbrook Nature Sanctuary, an extremely beautifull park along the coast of the Hudson. Something that was very surprising to me was that near the end of the route you literally cross back into New York! At this point, you are very close to the end.';

let storyWords = story.split(' ');
let unnecessaryWord = 'literally';
let misspelledWord = 'beautifull';
let badWord = 'freaking';

//console.log(storyWords);

let count = 0;
storyWords.forEach((word) => {
    count++;
});

console.log(count);
  
storyWords = storyWords.filter((word) => {
    return word !== unnecessaryWord;
});

storyWords = storyWords.map((word) => {
    return word === misspelledWord ? 'beautiful': word;
});

let badWordIndex = storyWords.findIndex((word) => {
    return word === badWord;
});

console.log(badWordIndex);

storyWords[78] = 'really';

let lengthCheck = storyWords.every((word) => {
    return word.length < 10;
});

console.log(lengthCheck);

storyWords.forEach((word) => {
    word.length > 10 && console.log(word);
})

let longWordIndex = storyWords.findIndex((word) => {
    return word.length > 10;
});

console.log(longWordIndex);

storyWords[111] = 'stunning';

console.log(storyWords.join(' '))
  
