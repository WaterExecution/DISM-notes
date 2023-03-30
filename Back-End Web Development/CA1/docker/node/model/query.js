/////////////////////////////////
// Name: Tong Yew Ching Kelvin //
// Admission: 2136871          //
// Class: DISM/FT/2B/21        //
/////////////////////////////////

var db = require('../config/databaseConfig.js');


// Insert modified to not create gaps from error
// Delete creates gap not recommended to shift ids, filling gaps is preferrable but increases complexity

class Database_query{
   constructor(){}
   async getUsers(callback) {
    var conn = db.getConnection();
    conn.connect(function (err) {
        if (err) {
            //console.log(err);
            return callback(err,null);
        }
        else {
            var sql = "SELECT userid, username, email, contact, role, profile_pic_url, DATE_FORMAT(created_at, '%Y-%m-%d %H:%i:%s') AS 'created_at' FROM SP_AIR.user";
            conn.query(sql, function (err, result) {
                conn.end();
                if (err) {
                    //console.log(err);
                    return callback(err, null);
                } else {
                    return callback(null, result);
                }
            });
        }
          });
   }
   async addUser(username, email, contact, password, role, profile_pic_url, callback) {
    var conn = db.getConnection();
    conn.connect(function (err) {
        if (err) {
            //console.log(err);
            return callback(err,null);
        }
        else {
            // Remove gaps from insert error, innodb_autoinc_lock_mode not best practise
            var sql = `INSERT INTO SP_AIR.user (username, email, contact, password, role, profile_pic_url)
                       SELECT  ?, ?, ?, ?, ?, ? FROM DUAL
                       WHERE NOT EXISTS(
                            SELECT NULL
                            FROM SP_AIR.user
                            WHERE username=? OR email=?
                            )
                       LIMIT 1;`;
            conn.query(sql, [username, email, contact, password, role, profile_pic_url, username, email], function (err, result) {
                conn.end();
                if (err) {
                    //console.log(err);
                    return callback(err, null);
                } else {
                    return callback(null, result);
                }
            });
        }
          });
   }
   async getUser(userid, callback) {
    var conn = db.getConnection();
    conn.connect(function (err) {
        if (err) {
            //console.log(err);
            return callback(err,null);
        }
        else {
            var sql = `SELECT userid, username, email, contact, role, profile_pic_url, DATE_FORMAT(created_at, '%Y-%m-%d %H:%i:%s') AS 'created_at'
                       FROM SP_AIR.user
                       WHERE userid=?`;
            conn.query(sql, [userid], function (err, result) {
                conn.end();
                if (err) {
                    //console.log(err);
                    return callback(err, null);
                } else {
                    return callback(null, result);
                }
            });
        }
          });
   }
   async updateUser(username, email, contact, password, role, profile_pic_url, userid, callback) {
    var conn = db.getConnection();
    conn.connect(function (err) {
        if (err) {
            //console.log(err);
            return callback(err,null);
        }
        else {
            var sql = `UPDATE SP_AIR.user
                       SET username=?, email=?, contact=?, password=?, role=?, profile_pic_url=?
                       WHERE userid=?`;
            conn.query(sql, [username, email, contact, password, role, profile_pic_url, userid], function (err, result) {
                conn.end();
                if (err) {
                    //console.log(err);
                    return callback(err, null);
                } else {
                    return callback(null, result);
                }
            });
        }
          });
   }
   async getAirports(callback) {
    var conn = db.getConnection();
    conn.connect(function (err) {
        if (err) {
            //console.log(err);
            return callback(err,null);
        }
        else {
            var sql = 'SELECT airportid, name, country FROM SP_AIR.airport';
            conn.query(sql, function (err, result) {
                conn.end();
                if (err) {
                    //console.log(err);
                    return callback(err, null);
                } else {
                    return callback(null, result);
                }
            });
        }
          });
   }
   async addAirport(name, country, description, callback) {
    var conn = db.getConnection();
    conn.connect(function (err) {
        if (err) {
            //console.log(err);
            return callback(err,null);
        }
        else {
            //Duplicate column name SELECT * FROM (SELECT ?, ?, ?, ? ,? ,?, ?) AS tmp
            var sql = `INSERT INTO SP_AIR.airport (name, country, description)
                       SELECT ?, ?, ? FROM DUAL
                       WHERE NOT EXISTS(
                            SELECT NULL
                            FROM SP_AIR.airport
                            WHERE name=?
                            )
                       LIMIT 1;`;
            conn.query(sql, [name, country, description, name], function (err, result) {
                conn.end();
                if (err) {
                    //console.log(err);
                    return callback(err, null);
                } else {
                    return callback(null, result);
                }
            });
        }
          });
   }
   async addFlight(flightCode, aircraft, originAirport, destinationAirport, embarkDate, travelTime, price, callback) {
    var conn = db.getConnection();
    conn.connect(function (err) {
        if (err) {
            //console.log(err);
            return callback(err,null);
        }
        else {
            //remove NOT exists to check ignore non existent airports
            var sql = `INSERT INTO SP_AIR.flight (flightCode, aircraft, originAirport, destinationAirport, embarkDate, travelTime, price)
                       SELECT ?, ?, ?, ? ,? ,?, ? FROM DUAL
                       WHERE EXISTS(
                       SELECT NULL
                            FROM SP_AIR.airport
                            WHERE airportid IN (?, ?)
                            )
                       LIMIT 1;`;
            conn.query(sql, [flightCode, aircraft, originAirport, destinationAirport, embarkDate, travelTime, price, originAirport, destinationAirport], function (err, result) {
                conn.end();
                if (err) {
                    //console.log(err);
                    return callback(err, null);
                } else {
                    //console.log(result)
                    return callback(null, result);
                }
            });
        }
          });
   }
   async getFlightDirect(originAirport, destinationAirport, callback) {
    var conn = db.getConnection();
    conn.connect(function (err) {
        if (err) {
            //console.log(err);
            return callback(err,null);
        }
        else {
            //Do not change WHERE (NOT) EXISTS import!
            var sql = `SELECT flightId,
                       flightcode,
                       aircraft,
                       (SELECT name FROM SP_AIR.airport WHERE airportId=flight.originAirport) AS 'originAirport',
                       (SELECT name FROM SP_AIR.airport WHERE airportId=flight.destinationAirport) AS 'destinationAirport',
                       embarkDate,
                       travelTime,
                       price
                       FROM SP_AIR.flight
                       WHERE flight.originAirport=? AND flight.destinationAirport=?`;
            conn.query(sql, [originAirport, destinationAirport], function (err, result) {
                conn.end();
                if (err) {
                    //console.log(err);
                    return callback(err, null);
                } else {
                    return callback(null, result);
                }
            });
        }
          });
   }
   async deleteFlight(flightId, callback) {
    var conn = db.getConnection();
    conn.connect(function (err) {
        if (err) {
            //console.log(err);
            return callback(err,null);
        }
        else {
            // DONT NOT CHANGE FLIGHTID OF EXISTING FLIGHTS!!! if flightid is printed on paper, it is no longer valid
            var sql = `DELETE FROM SP_AIR.flight
                       WHERE flightId=?`;
            conn.query(sql, [flightId], function (err, result) {
                conn.end();
                if (err) {
                    //console.log(err);
                    return callback(err, null);
                } else {
                    return callback(null, result);
                }
            });
        }
          });
   }
   async bookFlight(name, passport, nationality, age, userId, flightId, callback) {
    var conn = db.getConnection();
    conn.connect(function (err) {
        if (err) {
            //console.log(err);
            return callback(err,null);
        }
        else {
            // Ignore duplicate flightid from same userid, family buying possibility
            var sql = `INSERT INTO SP_AIR.booking (name, passport, nationality, age, fk_userId, fk_flightId)
                       VALUES (?, ?, ?, ?, ?, ?)`;
            conn.query(sql, [name, passport, nationality, age, userId, flightId], function (err, result) {
                conn.end();
                if (err) {
                    //console.log(err);
                    return callback(err, null);
                } else {
                    return callback(null, result);
                }
            });
        }
          });
   }
   async getFlightTransfer(originAirport, destinationAirport, callback) {
    var conn = db.getConnection();
    conn.connect(function (err) {
        if (err) {
            //console.log(err);
            return callback(err,null);
        }
        else {
            // Could be optimized, focused on readability
            var sql = `SELECT flight1.flightId AS                           "firstFlightId",
                       flight2.flightId AS                                  "secondFlightId",
                       flight1.flightCode AS                                "flightCode1",
                       flight2.flightCode AS                                "flightCode2",
                       flight1.aircraft AS                                  "aircraft1",
                       flight2.aircraft AS                                  "aircraft2",
                       (SELECT name
                       FROM SP_AIR.airport
                       WHERE airportId=flight1.originAirport) AS            "originAirport",
                       (SELECT name
                       FROM SP_AIR.airport
                       WHERE airportId=flight2.originAirport) AS            "transferAirport",
                       (SELECT name
                       FROM SP_AIR.airport
                       WHERE airportId=flight2.destinationAirport) AS       "destinationAirport",
                       (flight1.price+flight2.price) AS                     "Total price"
                       
                       FROM SP_AIR.flight flight1
                       INNER JOIN SP_AIR.flight flight2
                       
                       WHERE flight1.destinationAirport = flight2.originAirport
                       AND flight1.originAirport=?
                       AND flight2.destinationAirport=?`;

            conn.query(sql, [originAirport, destinationAirport], function (err, result) {
                conn.end();
                if (err) {
                    //console.log(err);
                    return callback(err, null);
                } else {
                    return callback(null, result);
                }
            });
        }
          });
   }
}

module.exports = Database_query;