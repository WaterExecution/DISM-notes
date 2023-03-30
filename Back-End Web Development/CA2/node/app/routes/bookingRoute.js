
const express = require('express');
const router = express.Router()

const bookingController = require("../controller/bookingController.js");

router.use(express.json());
router.use(express.urlencoded({extended:true}));

router.post('/booking/:userid/:flightid', bookingController.createBooking);

module.exports = router;
