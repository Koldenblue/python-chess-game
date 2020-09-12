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

        // TODO: could just validate input here 
        
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





