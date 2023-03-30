const jwt = require("jsonwebtoken")

const config = require("../config/authConfig.js");

const userModel = require("../model/userModel.js");

const hash = require("../middleware/hasher.js")
const auth = require("../middleware/auth.js")

exports.login = (req, res) => {
	
	var username = req.body.username
	var password = req.body.password;
	
	userModel.findOne({
		where: {
            username: username,
        },
	})
	.then(async (result) => {
		if (!result) {
			return res.status(404).send("Invalid Username or Password!");
	    }
		
		if (!hash.verifyPassword(password, result.dataValues.password)) {
			return res.status(404).send("Invalid Username or Password!");
		}
		
		var token = auth.getToken(result.dataValues.userid, result.dataValues.role)
		
		res.cookie('jwt', token, { httpOnly: true})
		if (result.dataValues.role === "Admin"){
			return res.status(200).json({"path":"admin.html"});
		}
		else{
			return res.status(200).json({"path":"flight.html"});
		}
	})
	.catch((error) => {
		// add logging
		console.log(error);
		return res.status(500).send("Internal Server Error");
	});
};

exports.refresh = (req, res) => {
	
	try {
		auth.refreshToken(req, res)
	}
	catch (err) {
		// add logging
		console.log(err);
		return res.status(500).send("Internal Server Error");
	}
};



exports.logout = (req, res) => {
	
	try {	
		res.clearCookie('jwt');
		res.redirect('/index.html')
	}
	catch (err) {
		// add logging
		console.log(err);
		return res.status(500).send("Internal Server Error");
	}
};
