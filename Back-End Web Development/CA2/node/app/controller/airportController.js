const airportModel = require("../model/airportModel.js");

exports.getAirports = (req, res) => {
	airportModel.findAll({
		attributes: ["airportid", "name", "country", "description"],
	})
	.then((result) => {
		return res.json(result);
	})
	.catch((error) => {
		// add logging
		// console.log(error);
		return res.status(500).send("Internal Server Error");
	});
};

exports.createAirport = (req, res) => {
	
	var name = req.body.name;
	var country = req.body.country;
	var description = req.body.description;
	
	//validate against "" strings
	
	airportModel.create({
		name: name,
		country: country,
		description: description,
	})
	.then((result) => {
		return res.status(200).json({"Message":"Success"});
	})
	.catch((error) => {
		try {
			if (error.parent.code === 'ER_DUP_ENTRY'){
				return res.status(422).send("Unprocessable Entity");
			}
		}
		catch {
			// add logging
			// console.log(error);
			return res.status(500).send("Internal Server Error");	
		}
	});

};