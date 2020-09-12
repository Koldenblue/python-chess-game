const pythonFilenames = ["py", "python3", "python"]
// pythonFile is the array index to use from the above array (pythonFilenames). This variable is global so that it is stored persistently.
let pythonFile = 0;
const { spawn } = require("child_process");     // for connecting to python file


module.exports = function(app) {

app.get("/api/python/start", (req, res) => {
    console.log("starting");
    startGame().then(() => {
        console.log("started")
    })
})

app.get("/api/python/:moveInput", (req, res) => {
    console.log("hi");
    console.log(req.params);
    res.status(200).end()
});
}

/** Input the moves for the chess game.
 * @param {string} move - A string from a1 thru h8 representing board positions. */
function startGame() {
    return new Promise((resolve, reject) => {
        let args = ["../../src/main"]     // array of argument vectors. The first argument vector is the python filepath.

        // try to run different terminal commands one at a time ["py", "python3", "python"]. These may vary depending on computer.
        spawnPython(pythonFilenames[pythonFile], args).then(() => resolve())
        .catch((err) => {
            spawnPython(pythonFilenames[++pythonFile], args).then(() => resolve())
        }).catch((err) => {
            spawnPython(pythonFilenames[++pythonFile], args).then(() => resolve())
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

let foundPython = false;  // bool that gets set to true once proper python installation is found. Global so that it is persistent.

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
        resolve();
    })
}