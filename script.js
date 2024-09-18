"use strict";
var goal_weight = 50000;
var num_females = 20;
var num_males = 20;
var start_min_weight = 200;
var start_max_weight = 600;
var start_male_average = 350;
var start_female_average = 250;
var mutate_prob = 0.01;
var mutate_min = .5;
var mutate_max = 1.2;
var litter_max = 8;
var generation_limit = 500;
var l = 5;
var d = 0;
var o = 0;
var num = 0;
var difference = 0;
var ratoverload = 0;
var generations = 0;
let parent_male_rats = [];
let parent_female_rats = [];
let babyrats = [];
let Mbabyrats = [];
let Fbabyrats = [];
function randomInt(min, max) {
    // min and max included 
    return Math.floor(Math.random() * (max - min + 1) + min);
}
;
function mutate() {
    var num = Math.random();
    if (num < mutate_prob) {
        var mutation = randomInt(mutate_min, mutate_max);
        num = mutation;
        return num;
    }
    else {
        num = 1;
        return num;
    }
}
function shuffle(array = []) {
    let currentIndex = array.length, randomIndex;
    // While there remain elements to shuffle.
    while (currentIndex != 0) {
        // Pick a remaining element.
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex--;
        // And swap it with the current element.
        [array[currentIndex], array[randomIndex]] = [
            array[randomIndex], array[currentIndex]
        ];
    }
    return array;
}
;
//first set of male rats
for (let i = 0; i < l; i++) {
    const rndInt = randomInt(start_min_weight, start_max_weight);
    parent_male_rats[parent_male_rats.length] = rndInt;
}
;
//first set of female rats
for (let i = 0; i < l; i++) {
    const rndInt = randomInt(start_min_weight, start_max_weight);
    parent_female_rats[parent_female_rats.length] = rndInt;
}
;
console.log("first", parent_male_rats);
console.log("first", parent_female_rats);
//sorts first rats into biggest to smallest values
parent_male_rats.sort((a, b) => b - a);
parent_female_rats.sort((a, b) => b - a);
//loop starts here?
for (let f = 0; f < 500; f++) {
    //to determine length for everything else
    if ((parent_male_rats.length > parent_female_rats.length) || (parent_male_rats.length = parent_female_rats.length)) {
        l = parent_male_rats.length;
    }
    else {
        l = parent_female_rats.length;
    }
    parent_male_rats = shuffle(parent_male_rats);
    parent_female_rats = shuffle(parent_female_rats);
    //for every item in the list
    for (let i = 0; i < l; i++) {
        //random litter size
        const littersize = randomInt(0, 8);
        //takes two parents and generates a number based on the two(does this for the random litter)
        for (let j = 0; j < littersize; j++) {
            const rndInt = randomInt(parent_female_rats[i], parent_male_rats[i]);
            babyrats[babyrats.length] = rndInt;
        }
        ;
    }
    for (let k = 0; k < babyrats.length; k++) {
        //ask Andy why I had to do the bob thing
        //this is what decides the gener of the baby rats
        const cointoss = randomInt(0, 1);
        let bob = 0;
        let thenum = mutate();
        babyrats[k] = (babyrats[k] * thenum);
        if (bob = cointoss) {
            Mbabyrats[Mbabyrats.length] = babyrats[k];
        }
        else {
            Fbabyrats[Fbabyrats.length] = babyrats[k];
        }
    }
    Mbabyrats.sort((a, b) => b - a);
    Fbabyrats.sort((a, b) => b - a);
    parent_male_rats = [];
    parent_female_rats = [];
    parent_male_rats = Mbabyrats;
    parent_female_rats = Fbabyrats;
    Mbabyrats = [];
    Fbabyrats = [];
    console.log("final", parent_male_rats);
    console.log("final", parent_female_rats);
    parent_male_rats.sort((a, b) => b - a);
    parent_female_rats.sort((a, b) => b - a);
    console.log(parent_male_rats.length);
    console.log(parent_female_rats.length);
    if (parent_male_rats.length != parent_female_rats.length) {
        if (parent_male_rats.length > parent_female_rats.length) {
            console.log("males is larger");
            difference = (parent_male_rats.length - parent_female_rats.length);
            for (let z = 0; z < difference; z++) {
                parent_male_rats.pop();
            }
        }
        else {
            console.log("female is longer");
            difference = (parent_female_rats.length - parent_male_rats.length);
            for (let z = 0; z < difference; z++) {
                parent_female_rats.pop();
            }
        }
    }
    else {
        console.log("they are the same");
    }
    ratoverload = (parent_female_rats.length - 20);
    console.log("ratoverload:", ratoverload);
    if (ratoverload > 0) {
        for (let p = 0; p < ratoverload; p++) {
            parent_male_rats.pop();
            parent_female_rats.pop();
        }
    }
    num = mutate();
    console.log("male", parent_male_rats);
    console.log("female", parent_female_rats);
    console.log("generations:", generations + 1);
    generations += 1;
    console.log("Largest Male:", parent_male_rats[0]);
    console.log("Largest Female:", parent_female_rats[0]);
    //if((parent_male_rats[0] >= 50000)||(parent_female_rats[0]>=50000))
    //{
    // f = 500
    //}
}
