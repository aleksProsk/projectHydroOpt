var express = require('express')
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  var isAjaxRequest = req.xhr;
  console.log('Some request');
  if (isAjaxRequest)
  {
	console.log('Ajax request');
  }
  else
  {
	res.render('index', { title: 'Expresss' });
	console.log('Request(originalURL = %s, baseURL = %s, IP = %s, IPS = %s, hostname = %s, body = %s)', req.originalURL, req.baseURL, req.ip, req.ips, req.hostname, req.body.toString());  
  }
});


router.get('/secretpath', function(req, res, next) {
  res.render('secretindex', { title: 'the secret path' });
  console.log('Request(originalURL = %s, baseURL = %s, IP = %s, IPS = %s, hostname = %s, body = %s)', req.originalURL, req.baseURL, req.ip, req.ips, req.hostname, req.body.toString());  
});

router.get('/process_get', function (req, res) {
	console.log('process_get');
	// Prepare output in JSON format
	response = {
	first_name:req.query.first_name,
	last_name:req.query.last_name
	};
	console.log(response);
	res.end(JSON.stringify(response));
});

var bodyParser = require('body-parser');
var urlencodedParser = bodyParser.urlencoded({ extended: false });
router.post('/process_post', urlencodedParser, function (req, res) {
	console.log('process_post');
	// Prepare output in JSON format
	response = {
	first_name:req.body.first_name,
	last_name:req.body.last_name
	};
	console.log(response);
	res.end(JSON.stringify(response));
});

router.post('/', urlencodedParser, 
	function (req, res) 
	{
		console.log('POST');
		var isAjaxRequest = (req.xhr || req.headers.accept.indexOf('json') > -1);
		if (isAjaxRequest)
		{
			console.log('AJAX POST');
			
			console.log(req.body);			
			input = req.body;
			console.log(input.first_name);			
			response = {first_name:input.first_name, last_name:input.last_name};

			console.log(response);
			res.end(JSON.stringify(response));			
		}
		else
		{
			console.log('NON-AJAX POST');			
		}
	}
);

router.get('/get_timeseries', 
	function (req, res) 
	{
		var yearStr = req.query.year;
		console.log('get_timeseries');
		response = 
		{
			year:	yearStr,
			path:	'C:/Users/Christoph/Documents/preise/power/'+yearStr+'/energy_spot_historie_'+yearStr+'.xls'
		};
		console.log(response);
		var fs = require("fs");
		if (fs.existsSync(response.path))
		{
			res.download(response.path,'eex_spot_'+yearStr+'.xls',
				function(err)
				{
					if (err) 
					{				
						res.status(404).end();				
						return console.error(err);
					}
					else
					{
						console.log('Success');
						res.end();
					}
				});
		}
		else
		{
			console.log('Invalid date');
			res.end();
		}
	}
);

module.exports = router;
