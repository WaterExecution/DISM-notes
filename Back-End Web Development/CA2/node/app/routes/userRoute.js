
const express = require('express');
const router = express.Router()

const auth = require("../middleware/auth.js")

const userController = require("../controller/userController.js");

router.use(express.json());
router.use(express.urlencoded({extended:true}));

// router.get("/user/:id", userController.getUser);

router.get("/user", [auth.verifyToken, userController.getUser]);

router.post('/users', userController.createUser);

router.put('/users', [auth.verifyToken, userController.updateUser]);

module.exports = router;
