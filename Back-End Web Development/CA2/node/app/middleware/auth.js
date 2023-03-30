const jwt = require("jsonwebtoken")
const jwt_decode = require('jwt-decode');
const config = require("../config/authConfig.js");

const catchError = (err, res) => {
  if (err instanceof jwt.TokenExpiredError) {
    return res.redirect('/login.html')
  }

  return res.redirect('/login.html')
}

const getToken = (userid, role) => {
	try {
		const token = jwt.sign({ id: userid, role: role,}, config.secret, {
			expiresIn: config.jwtExpiration
		});
		return token
	}
	catch (err) {
		console.log(err);
		return
	}
}

const verifyToken = (req, res, next) => {
  try {
	var token = req.cookies.jwt;
  }
  catch(err) {
    return res.redirect('/login.html')
  }

  jwt.verify(token, config.secret, (err, decoded) => {
    if (err) {
      return catchError(err, res);
    }
    return next();
  });
};

const refreshToken = (req, res, next) => {
  try {
	var token = req.cookies.jwt;
  }
  catch(err) {
    return res.redirect('/login.html')
  }

  jwt.verify(token, config.secret, (err, decoded) => {
    if (err) {
      return catchError(err, res);
    }
    else {
		var newToken = getToken(jwt_decode(token).id);
		res.cookie('jwt', newToken, { httpOnly: true})
		return res.status(200).json({"Message":"Success"});
	}
  });
};

const checkRole = (req, res, next) => {
  try {
	var token = req.cookies.jwt;
  }
  catch(err) {
    return res.redirect('/login.html')
  }

  jwt.verify(token, config.secret, (err, decoded) => {
    if (err) {
      return catchError(err, res);
    }
    else {
		var role = jwt_decode(token).role;
		if (role === "Admin"){
			return next()
		}
		else{
			return res.redirect('/login.html')
		}
	}
  });
};

const auth = {
  verifyToken: verifyToken,
  refreshToken: refreshToken,
  getToken: getToken,
  checkRole: checkRole,
};

module.exports = auth
