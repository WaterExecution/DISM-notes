/////////////////////////////////
// Name: Tong Yew Ching Kelvin //
// Admission: 2136871          //
// Class: DISM/FT/2B/21        //
/////////////////////////////////

const express        = require('express');
const app          = express();
const Database_query = require('../model/query.js')
const product = require('../model/product.js')
const upload = require("../middleware/fileUpload.js")

const query = new Database_query()
const productAPI = new product()

app.use(express.json());
app.use(express.urlencoded({extended:false}));
app.disable('etag');
app.disable('x-powered-by');

//app.get('/', function (req, res) {
//	return res.render('index.html');
//});

app.get('/users', function (req, res) {
 query.getUsers(function (err, result) {
  if (!err) {
    res.send(result);
  }else{
    res.status(500).send("Internal Server Error");
  }
 });
});

app.post('/users', function (req, res) {

  var username = req.body.username;
  var email = req.body.email;
  var contact = req.body.contact;
  var password = req.body.password;
  var role = req.body.role;
  var profile_pic_url = req.body.profile_pic_url;

  query.addUser(username, email, contact, password, role, profile_pic_url, function (err, result) {
    if (result.affectedRows == 0) {
      res.status(422).send("Unprocessable Entity");
    } else if (!err) {
      res.status(201).json({"userid":result.insertId});
    }else{
      res.status(500).send("Internal Server Error");
    }
   });
});

app.get('/users/:id', function (req, res) {
  
  var id = req.params.id

  query.getUser(id, function (err, result) {
    if (!err) {
      res.send(result);
    }else{
      res.status(500).send("Internal Server Error");
    }
   });
});

app.put('/users/:id', function (req, res) {

  var username = req.body.username;
  var email = req.body.email;
  var contact = req.body.contact;
  var password = req.body.password;
  var role = req.body.role;
  var profile_pic_url = req.body.profile_pic_url;
  var id = req.params.id

  query.updateUser(username, email, contact, password, role, profile_pic_url, id, function (err, result) {
    if (!err) {
      res.status(204).send("No Content");
    } else if (err.code == 'ER_DUP_ENTRY') {
      res.status(422).send("Unprocessable Entity");
    }else{
      res.status(500).send("Internal Server Error");
    }
   });
});

app.get('/airport', function (req, res) {
  query.getAirports(function (err, result) {
    if (!err) {
      res.send(result);
    }else{
      res.status(500).send("Internal Server Error");
    }
   });
});

app.post('/airport', function (req, res)  {

  var name = req.body.name;
  var country = req.body.country;
  var description = req.body.description;

  query.addAirport(name, country, description, function (err, result) {
    if (result.affectedRows == 0) {
      res.status(422).send("Unprocessable Entity");
    } else if (!err) {
      res.status(204).send("No Content");
    }else{
      res.status(500).send("Internal Server Error");
    }
   });
});

app.post('/flight', function (req, res) {

  var flightCode = req.body.flightCode;
  var aircraft = req.body.aircraft;
  var originAirport = req.body.originAirport;
  var destinationAirport = req.body.destinationAirport;
  var embarkDate = req.body.embarkDate;
  var travelTime = req.body.travelTime;
  var price = req.body.price;

  query.addFlight(flightCode, aircraft, originAirport, destinationAirport, embarkDate, travelTime, price, function (err, result) {
    if (result.affectedRows == 0) {
      res.status(500).send("Internal Server Error");
    } else if (!err) {
      res.status(201).json({"flightid":result.insertId});
    }else{
      res.status(500).send("Internal Server Error");
    }
   });
});

app.get('/flightDirect/:originAirportId/:destinationAirportId', function (req, res)  {
  var originAirportId = req.params.originAirportId
  var destinationAirportId = req.params.destinationAirportId

  query.getFlightDirect(originAirportId, destinationAirportId, function (err, result) {
    if (!err) {
      res.status(200).send(result);
    }else{
      res.status(500).send("Internal Server Error");
    }
   });
});

app.delete('/flight/:id', function (req, res)  {

  var id = req.params.id

  query.deleteFlight(id, function (err, result) {
    if (result.affectedRows == 0) {
      res.status(500).json({"Message":"Deletion fail"});
    } else if (!err) {
      res.status(200).json({"Message":"Deletion successful"});
    }else{
      res.status(500).send("Internal Server Error");
    }
   });
});

app.post('/booking/:userid/:flightid', function (req, res)  {

  var name = req.body.name;
  var passport = req.body.passport; //NRIC
  var nationality = req.body.nationality;
  var age = req.body.age;
  var userId = req.params.userid
  var flightId = req.params.flightid

  query.bookFlight(name, passport, nationality, age, userId, flightId, function (err, result) {
    if (!err) {
      res.status(201).json({"bookingid":result.insertId});
    }else{
      res.status(500).send("Internal Server Error");
    }
   });
});

app.get('/transfer/flight/:originAirportId/:destinationAirportId', function (req, res) {
  var originAirportId = req.params.originAirportId
  var destinationAirportId = req.params.destinationAirportId

  query.getFlightTransfer(originAirportId, destinationAirportId, function (err, result) {
    if (!err) {
      res.status(201).send(result);
    }else{
      res.status(500).send("Internal Server Error");
    }
   });
});

app.post('/upload', upload.single("image"), function (req, res) {
  var image = req.file
  var name = req.body.name
  if ((image.size <= 1048576) && (image.originalname.slice(-4) === ".jpg") || (image.originalname.slice(-4) === ".png")){
    productAPI.uploadImage(name, image, function (err, result) {
      if (!err) {
        res.status(200).json({"productid":result.insertId});
      }else{
        res.status(500).send("Internal Server Error");
      }
     });
  }else{
    res.status(500).send("Internal Server Error");
  }
});

app.get('/uploads', function (req, res) {
  productAPI.getImages(function (err, result) {
    if (!err) {
      res.status(200).send(result);
    }else{
      res.status(500).send("Internal Server Error");
    }
   });
});

app.get('/uploads/:id', function (req, res) {

  var productId = req.params.id

  productAPI.getImage(productId, function (err, result) {
    if (!err) {
      res.status(200).send(result);
    }else{
      res.status(500).send("Internal Server Error");
    }
   });
});


app.all('*', (req, res) => {
	return res.status(404).send({
		message: '404 page not found'
	});
});

module.exports = app;
