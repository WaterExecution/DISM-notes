
const express = require('express');
const router = express.Router()

const jwtController = require("../controller/jwtController.js")

router.use(express.json());
router.use(express.urlencoded({extended:true}));

router.post("/login", jwtController.login);

router.get("/refresh", jwtController.refresh);

router.get("/logout", jwtController.logout);

module.exports = router;
