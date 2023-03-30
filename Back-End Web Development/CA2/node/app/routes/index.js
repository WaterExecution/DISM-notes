const express = require('express');
const app = express()
const path = require('path');
const cookieParser = require("cookie-parser");
const cors = require("cors");


//const product = require('../model/product.js')
//const upload = require("../middleware/fileUpload.js")
const auth = require("../middleware/auth.js")

const userRoute = require("../routes/userRoute.js")
const airportRoute = require("../routes/airportRoute.js")
const flightRoute = require("../routes/flightRoute.js")
const bookingRoute = require("../routes/bookingRoute.js")
const jwtRoute = require("../routes/jwtRoute.js")

const corsOptions = {
  origin: "http://localhost:8080"
};

app.use(express.json());
app.use(express.urlencoded({extended:true}));
app.use(cookieParser())
//app.disable('etag');
//app.disable('x-powered-by');

app.use(function(req, res, next) {
	res.header(
	  "Access-Control-Allow-Headers",
	  "Authorization, Origin, Content-Type, Accept, x-requested-with"
	);
	res.header(
	  "Access-Control-Allow-Origin",
	  "http://localhost:8080"
	);
	next();
});

app.use('/', [userRoute, airportRoute, flightRoute, bookingRoute, jwtRoute])
app.use(express.static("app/public"));
app.use(auth.verifyToken, express.static("app/public/authenticated"));
app.use(auth.checkRole, express.static("app/public/admin"));

app.all('*', (req, res) => {
	return res.status(404).send({
		message: '404 page not found'
	});
});

module.exports = app;
