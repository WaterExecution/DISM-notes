const jwt_decode = require('jwt-decode');
const userModel = require("../model/userModel.js");
const hash = require("../middleware/hasher.js")

exports.getUser = (req, res) => {
	
	var id = jwt_decode(req.cookies.jwt).id;
	
	userModel.findOne({
		attributes: ["userid", "username", "email", "contact", "role", "profile_pic_url", "created_at"],
		where: {
            userid: id,
        },
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

// exports.getUsers = (req, res) => {
	// userModel.findAll({
		// attributes: ["userid", "username", "email", "contact", "role", "profile_pic_url", "created_at"],
	// })
	// .then((result) => {
		// return res.json(result);
	// })
	// .catch((error) => {
		// // add logging
		// // console.log(error);
		// return res.status(500).send("Internal Server Error");
	// });
// };

exports.createUser = (req, res) => {
	
	var username = req.body.username;
	var email = req.body.email;
	var password = hash.getHash(req.body.password); // check for password requirement
	var role = "Customer" // req.body.role; only admin should be able to modify role
	var profile_pic_url = req.body.profile_pic_url;
	
	userModel.create({
		username: username,
		email: email,
		password: password,
		role: role,
		profile_pic_url: profile_pic_url,
	})
	.then((result) => {
		return res.json({"userid":result.dataValues.userid});
	})
	.catch((error) => {
		//console.log(error)
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

exports.updateUser = (req, res) => {
	
	var username = req.body.username;
	var email = req.body.email;
	var contact = req.body.contact;
	var password = hash.getHash(req.body.password);
	var role = "Customer" // req.body.role; only admin should be able to modify role
	var profile_pic_url = req.body.profile_pic_url;
	
	var id = jwt_decode(req.cookies.jwt).id;
	
	userModel.update(
		{
			username: username,
			email: email,
			contact: contact,
			password: password,
			role: role,
			profile_pic_url: profile_pic_url,
		},
		{
			where: {
				userid: id,
			},
		}
	)
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