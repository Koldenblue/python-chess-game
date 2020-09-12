const submitBtn = $("#submit-move");
const movementForm = $("#movement-form")

$(document).ready(main)

function main() {
    addListeners();
    $("#move-input").focus();
}

function addListeners() {
    // add listener to submit movement form
    movementForm.on("submit", function(event) {
        event.preventDefault();
        console.log("hi")
        // toggle the submit confirmation text
        $("h2").slideToggle("slow");
        setTimeout(() => {
            $("h2").slideToggle("slow");
        },
        1000)
        console.log($("#move-input"))

        // send form value
        console.log($("#move-input").val())
        let moveInput = $("#move-input").val();
        let queryUrl = '/api/python/' + moveInput 
        $.ajax({
            url: queryUrl,
            method: "GET"
        }).then((result) => {
            console.log(result);
        })
    });
}






const pythonFilenames = ["py", "python3", "python"]
// pythonFile is the array index to use from the above array (pythonFilenames). This variable is global so that it is stored persistently.
let pythonFile = 0;

/** Input the moves for the chess game. */
function inputMoves() {

}

function formatDataTable(columns) {
    return new Promise((resolve, reject) => {
        let args = ["./nodePythonApp/formatter.py"]     // array of argument vectors. The first argument vector is the python filepath.
        // add column header names to argument vectors (these are the title of each column, derived from the object keys)
        for (let columnName in columns[0]) {
            args.push(columnName)
        }
        // Add in the second argument vector to be the number of columns to be formatted.
        let numColumns = args.length - 1;
        args.splice(1, 0, numColumns)
        // Now, args is the python filename, the number of columns, plus a list of the column headers.
        // Finally, add info for each object in the column to args list. These will become the table rows.
        for (let obj of columns) {
            for (let key in obj) {
                args.push(obj[key])
            }
        }

        // If python is installed, use python to format the table. If not, use JavaScript.
        if (pythonInstalled) {
            spawnPython(pythonFilenames[pythonFile], args).then(data => {
                resolve(data);
            })
            // try to run different terminal commands one at a time ["py", "python3", "python"]. These may vary depending on computer.
            .catch((err) => {
                pythonFile++;
                spawnPython(pythonFilenames[pythonFile], args).then(data => {
                    resolve(data);
                }).catch((err) => {
                    pythonFile++;
                    spawnPython(pythonFilenames[pythonFile], args).then(data => {
                        resolve(data);
                    }).catch((err) => {
                        reject("Error: Could not find python filepath. Changing configuration to use JavaScript instead.");
                    })
                })
            })
        }
        
        // if python is not installed or cannot be found, can still use the same args list.
        // This code block is roughly equivalent to the code in the formatter.py file
        if (!pythonInstalled) {
            columnCounter = 0;
            // args[1] is the number of columns. starting at args[2] is the data to go in each column
            let rowStr = "";
            let columnLength = 25;      // the max width of a column in the table
            // create formatted table and store in a string:
            for (let i = 2, j = args.length; i < j; i++) {
                let truncatedArg = args[i].toString().slice(0, columnLength);
                rowStr += truncatedArg;
                let remainingLength = columnLength - truncatedArg.length;
                for (let i = 0; i < remainingLength; i++) {
                    rowStr += " ";
                }
                rowStr += " ";
                columnCounter++;
                if (columnCounter % Number(args[1]) === 0) {
                    rowStr += "\n"
                }
                if (columnCounter === Number(args[1])) {
                    let headerStr = ""
                    for (let i = 0; i < Number(args[1]); i++) {
                        for (let j = 0; j < columnLength; j++) {
                            headerStr += "_";
                        }
                    }
                    headerStr += "\n";
                    rowStr += headerStr;
                }
            }
            resolve(rowStr)
        }
    }).catch((err) => {
        // if cannot find python, try again without python
        if (err === "Error: Could not find python filepath. Changing configuration to use JavaScript instead.") {
            console.log(err);
            pythonInstalled = false;
            formatDataTable(columns)
        }
        else {
            connection.end();
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
        // on data event emitted by python program, resolve promise.
        py.stdout.on('data', (data) => {
            data = data.toString();
            foundPython = true;
            resolve(data);
        })
        // If system hangs due to permission error, etc, wait to see if python file has been found before returning promise rejection
        setTimeout(() => {
            if (!foundPython) {
                console.log("Searching for python filepath...")
                reject("Improper python path.");
            }
        }, 1500);
    })
}
