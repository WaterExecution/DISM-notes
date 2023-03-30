const bcrypt = require("bcrypt");

const saltRounds = 10;
  
exports.getHash = (password) => {
	try {
		return bcrypt.hashSync(password, saltRounds)
	}
	catch (err) {
		//console.log(err);
		return
	}
};

exports.verifyPassword = (password, hash) => {
	try {
		return bcrypt.compareSync(password, hash)
	}
	catch (err) {
		//console.log(err);
		return
	}
};