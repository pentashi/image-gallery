import { greet } from 'index.htm';

console.log(greet('achapi'))

const salutation = (name, age) => `hello ${name} you are ${age} years old todau`
console.log(salutation('achapi', 20))
// assyn/await

const fetchData = assync() = {
    const response = await fetch('https://google.com');
    const data = await response.json();
    console.log(data);
}
fetchData();