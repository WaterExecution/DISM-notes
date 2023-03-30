const { QueryTypes } = require("sequelize");
const sequelize = require("../config/databaseConfig.js");

const flightModel = require("../model/flightModel.js");

exports.getFlights = (req, res) => {
	sequelize.query(`SELECT flightId,
                       flightcode,
                       aircraft,
                       (SELECT name FROM SP_AIR.airports WHERE airportId=flights.originAirport) AS 'originAirport',
                       (SELECT name FROM SP_AIR.airports WHERE airportId=flights.destinationAirport) AS 'destinationAirport',
                       embarkDate,
                       travelTime,
                       price
                       FROM SP_AIR.flights`,
					   {
						type: QueryTypes.SELECT
						},
	)
	.then((result) => {
		return res.json(result);
	})
	.catch((error) => {
		// add logging
		// console.log(error);
		return res.status(500).send("Internal Server Error");
	});
};

exports.getFlight = (req, res) => {
	
	var originAirportId = req.params.originAirportId
	var destinationAirportId = req.params.destinationAirportId
	
	sequelize.query(`SELECT flightId,
                       flightcode,
                       aircraft,
                       (SELECT name FROM SP_AIR.airports WHERE airportId=flights.originAirport) AS 'originAirport',
                       (SELECT name FROM SP_AIR.airports WHERE airportId=flights.destinationAirport) AS 'destinationAirport',
                       embarkDate,
                       travelTime,
                       price
                       FROM SP_AIR.flights
                       WHERE flights.originAirport= :originAirportId AND flights.destinationAirport= :destinationAirportId`,
					   {
						replacements: {originAirportId:originAirportId,destinationAirportId:destinationAirportId},
						type: QueryTypes.SELECT
						},
	)
	.then((result) => {
		return res.json(result);
	})
	.catch((error) => {
		// add logging
		console.log(error);
		return res.status(500).send("Internal Server Error");
	});
};

exports.getTransferFlight = (req, res) => {
	
	var originAirportId = req.params.originAirportId
	var destinationAirportId = req.params.destinationAirportId
	
	sequelize.query(`SELECT flight1.flightId AS                            "firstFlightId",
					   flight2.flightId AS                                 "secondFlightId",
					   flight1.flightCode AS                               "flightCode1",
					   flight2.flightCode AS                               "flightCode2",
					   flight1.aircraft AS                                 "aircraft1",
					   flight2.aircraft AS                                 "aircraft2",
					   (SELECT name
					   FROM SP_AIR.airports
					   WHERE airportId=flight1.originAirport) AS           "originAirport",
					   (SELECT name
					   FROM SP_AIR.airports
					   WHERE airportId=flight2.originAirport) AS           "transferAirport",
					   (SELECT name
					   FROM SP_AIR.airports
					   WHERE airportId=flight2.destinationAirport) AS      "destinationAirport",
					   flight1.travelTime AS                                "travelTime1",
					   flight2.travelTime AS                                "travelTime2",
					   flight1.embarkDate AS                                "embarkDate1",
					   flight2.embarkDate AS                                "embarkDate2",
					   (flight1.price+flight2.price) AS                     "Total price"

					   FROM SP_AIR.flights flight1
					   INNER JOIN SP_AIR.flights flight2

					   WHERE flight1.destinationAirport = flight2.originAirport
                       AND flight1.originAirport= :originAirportId
                       AND flight2.destinationAirport= :destinationAirportId`,
					   {
						replacements: {originAirportId:originAirportId,destinationAirportId:destinationAirportId},
						type: QueryTypes.SELECT
						},
	)
	.then((result) => {
		return res.json(result);
	})
	.catch((error) => {
		// add logging
		console.log(error);
		return res.status(500).send("Internal Server Error");
	});
};


exports.createFlight = (req, res) => {
	
	var flightCode = req.body.flightCode;
	var aircraft = req.body.aircraft;
	var originAirport = req.body.originAirport;
	var destinationAirport = req.body.destinationAirport;
	var embarkDate = req.body.embarkDate;
	var travelTime = req.body.travelTime;
	var price = req.body.price;
	
	flightModel.create({
		flightCode: flightCode,
		aircraft: aircraft,
		originAirport: originAirport,
		destinationAirport: destinationAirport,
		embarkDate: embarkDate,
		travelTime: travelTime,
		price: price,
	})
	.then((result) => {
		return res.status(201).json({"flightid":result.dataValues.flightId});
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


exports.deleteFlight = (req, res) => {
	
	var id = req.params.id
	
	flightModel.destroy({
		where: {
            flightId: id,
        },
	})
	.then((result) => {
		if (result == 1){
			return res.status(200).json({"Message":"Deletion successful"});
		}
		else{
			return res.status(500).json({"Message":"Deletion fail"});
		}
	})
	.catch((error) => {
		// add logging
		// console.log(error);
		return res.status(500).send("Internal Server Error");	
	});

};

