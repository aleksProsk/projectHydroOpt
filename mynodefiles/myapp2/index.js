// index.js
var express = require('express');  
var app = express();  

console.log('index-js')

app.get('/', function (req, res) {  
  res.send('Hello Wörld!')
  console.log('app.get( %s, %s)', req, res)
})

var server = app.listen(3000, function () {

  var host = server.address().address
  var port = server.address().port

  console.log('Example app listening at http://%s:%s', host, port)

})