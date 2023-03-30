const express = require('express');
const router = express.Router()

const auth = require("../middleware/auth.js")

const airportController = require("../controller/airportController.js");

router.use(express.json());
router.use(express.urlencoded({extended:true}));

router.get("/airport", airportController.getAirports);

router.post("/airport", auth.checkRole, airportController.createAirport);

module.exports = router;
