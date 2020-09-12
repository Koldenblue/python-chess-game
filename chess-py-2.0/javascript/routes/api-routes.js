module.exports = function(app) {

app.get("/api/python/:moveInput", (req, res) => {
    console.log("hi");
    console.log(req.params);
    res.status(200).end()
})
}