# Math
```
Math.PI
Math.floor()
Math.random()
Math.round()
f.toFixed()
```

# Operators
```
+ - * % ^
+= -= *= /= 
x++ x-- ++x --x
= < > ! == <= >= !=
&& ||
```

# Variables
```
var variable;
let preferredvariable;
const constant;
```

# Conversions
```
parseInt()
parseFloat()
.toString()
```

# Strings
```
s.slice()
s.repeat()
```

# I/O
```
const input = require('readline-sync');
input.question(""); input.questionInt("");
console.log(`x is ${x}`);
process.stdout.write(""); //For no newline, writes to stdout
```

# Selectors
```
if(){}
else if(){}
else{}
let x = (x > 1) ? true : (x > 2) ? true : false; //Is x > 1 and x > 2? else x = false;
```

# Repetitions
```
for(i=0;i<3;i++){} // 0 1 2
for(i=0;++i<=3;){} // 1 2 3
for (i=3; i--;){} // 2 1 0
while(i<3){}     // 0 1 2
do{}while()
for(num of numArray){}
```

# Arrays
```
var a = new Array(1); //Captial important!
var a = ['a','b'];
a.length
a.push
a.pop
a.join
Math.max()
Math.max.apply(Math, a) //For string
Math.min()
a.map(x => x+1)  //Adds one to each element
```

# Functions
```
function(){}
```

# Classes
```
class Circle {
  constructor(radius) {
    this.radius = radius;
  }
  getArea(){
	return Math.PI*this.radius**2
  }
}

var circle = new Circle(2);

console.log(circle.getArea());
```

# More Advanced
```
[...Array(10).keys()]
[...Array(10).keys()].slice(1)

# javascript has a max of 65535 arguments

Math.max(...numbers)
nums.reduce((acc, val) => { return acc > val ? acc : val; });
nums.reduce((a, b) => (a + b))
```