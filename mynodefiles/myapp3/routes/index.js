//Start via
////set DEBUG=myapp:* & npm start

var express = require('express');
var router = express.Router();
var fs = require('fs');
const path = require('path');

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('store', { title: 'Store 1' });
});

router.get('/store2', function(req, res, next) {
  res.render('store2', { title: 'Store 2' });
});


router.get('/store3', function(req, res, next) {
  res.render('store3', { title: 'Store 3' });
});


var child_process = require('child_process');
router.get("/search", function (req, res) {
	var searchStr = req.query.q;
	var cmd = 'findstr /M /I /c:"'+searchStr+' " C:\\cygwin64\\home\\Christoph\\bigcartel\\jsons\\*.json';
	var results = [];
	child_process.exec(cmd, {maxBuffer: 200000000}, function(err, stdout, stderr) 
	{
		var resultPaths = stdout.split('\r\n');
		var relevantProducts = [];
		var perStoreResults = [];
		resultPaths.forEach(function (pathStr) {		
			if (fs.existsSync(pathStr))
			{
				var storeStr = path.basename(pathStr).slice(0,-5).toUpperCase();
				var allProducts = JSON.parse(fs.readFileSync(pathStr, 'utf8'));
				var perStoreResult = {store: storeStr, allProducts: allProducts};
				
				allProducts.forEach(function (product) {
					if (JSON.stringify(product).includes(searchStr)) { 
						product.store = storeStr;
						relevantProducts.push(product); };
				});
				
				perStoreResults.push(perStoreResult);
			};
		});
		res.render('search', { title: 'Search results',  query: searchStr, perStoreResults: perStoreResults, productResults: relevantProducts.slice(0,6)});
	});	
});
/*
const fs = require('fs');
var obj = [];
var path = 'C:\\cygwin64\\home\\Christoph\\bigcartel\\jsons\\';
fs.readdir(path, (err, files) => {
  files.forEach(file => {
    console.log(file);
	try {var x = JSON.parse(fs.readFileSync(path+file,'utf8')); 	obj.push(x);}
	catch(e) {console.log('error reading');}
  });
})
*/

module.exports = router;
