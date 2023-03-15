const express = require('express');
const app = express();
const path = require('path');
const PORT = 3000;
 
// Serve react app (build folder)
app.use(express.static(path.join(__dirname, 'build')))
   
app.get('/healthz', function (req, res, next) {
    res.sendStatus(200);
});
 
app.listen(PORT, function(err){
    if (err) console.log(err);
    console.log("Express web server listening on port:", PORT);
});