const express = require('express');
const router = express.Router()

const auth = require("../middleware/auth.js")

const flightController = require("../controller/flightController.js");

router.use(express.json());
router.use(express.urlencoded({extended:true}));

router.get("/flights", flightController.getFlights);

router.get("/flightDirect/:originAirportId/:destinationAirportId", flightController.getFlight);

router.get("/transfer/flight/:originAirportId/:destinationAirportId", flightController.getTransferFlight);

router.post("/flight", auth.checkRole, flightController.createFlight);

// router.delete("/flight/:id", flightController.deleteFlight);

module.exports = router;
