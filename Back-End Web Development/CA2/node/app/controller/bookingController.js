
const bookingModel = require("../model/bookingModel.js");

exports.createBooking = (req, res) => {
	
	var name = req.body.name;
	var passport = req.body.passport; //NRIC
	var nationality = req.body.nationality;
	var age = req.body.age;
	var userid = req.params.userid
	var flightid = req.params.flightid
	
	bookingModel.create({
		name: name,
		passport: passport,
		nationality: nationality,
		age: age,
		fk_userid: userid,
		fk_flightid: flightid,
	})
	.then((result) => {
		return res.status(201).json({"bookingid":result.dataValues.bookingid});
	})
	.catch((error) => {
		// add logging
		console.log(error);
		return res.status(500).send("Internal Server Error");
	});

};
