const pythonFilenames = ["py", "python3", "python"]
// pythonFile is the array index to use from the above array (pythonFilenames). This variable is global so that it is stored persistently.
let pythonFile = 0;
const { spawn } = require("child_process");     // for connecting to python file



console.log("starting");
// startGame().then((py) => {
let args = ["../nodePythonApp/Main.py", "an argument"]
let py = spawn("python3", args).on('error', (err) => {
    reject("Improper python path.");
})
console.log("started")
// console.log(py)

py.stdout.on("data", (data) => {
    data = data.toString();
    console.log(data)
    console.log("z")
    
})
// console.log(py)
console.log(py.stdout._events.data)