const pythonFilenames = ["py", "python3", "python"]
// pythonFile is the array index to use from the above array (pythonFilenames). This variable is global so that it is stored persistently.
let pythonFile = 0;
const { spawn } = require("child_process");     // for connecting to python file



function start() {
    startGame().then((py) => {
        console.log(py)
        console.log(py.stdout._events.data)
        py.stdout.on("data", (data) => {
            data = data.toString();
            console.log(data)
            console.log("z")
        })
        console.log(py.stdout._events.data)
    });
}

start();



function startGame() {
    return new Promise((resolve, reject) => {
        let args = ["../nodePythonApp/Main.py"]     // array of argument vectors. The first argument vector is the python filepath.

        // try to run different terminal commands one at a time ["py", "python3", "python"]. These may vary depending on computer.
        spawnPython(pythonFilenames[pythonFile], args).then((py) => resolve(py))
        .catch((err) => {
            spawnPython(pythonFilenames[++pythonFile], args).then((py) => resolve(py))
        }).catch((err) => {
            spawnPython(pythonFilenames[++pythonFile], args).then((py) => resolve(py))
        }).catch((err) => {
            reject("Error: Could not find python filepath.");
        })
    }).catch((err) => {
        // if cannot find python, try again without python
        if (err === "Error: Could not find python filepath.") {
            console.log(err);
            reject(err);
        }
        else {
            reject(err);
        }
    })
}

let dataString = "x";
/** Spawn new python program designed to accept an array of arguments and format into a table.
 * On data event, return promised data (the formatted table) as a string
 * @param {array} args : An array in the format [python_script_name, number of columns, column data ...,]
 * @param {string} pythonFile : The command to access python in a terminal. This is usually "python3", "python", or "py"*/
function spawnPython(pythonFile, args) {
    return new Promise((resolve, reject) => {
        // run python using the command "<python> <argument vectors>"
        let py = spawn(pythonFile, args).on('error', (err) => {
            reject("Improper python path.");
        })

        resolve(py);
    })
}