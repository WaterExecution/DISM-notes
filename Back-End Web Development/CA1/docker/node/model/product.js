/////////////////////////////////
// Name: Tong Yew Ching Kelvin //
// Admission: 2136871          //
// Class: DISM/FT/2B/21        //
/////////////////////////////////

var db = require('../config/databaseConfig.js');

class product{
    constructor(){}
    async uploadImage(name, image, callback) {
        var conn = db.getConnection();
        conn.connect(function (err) {
            if (err) {
                //console.log(err);
                return callback(err,null);
            }
            else {
                var sql = 'INSERT INTO SP_AIR.product (name, path) VALUES (?, ?)';
                conn.query(sql, [name, image.filename], function (err, result) {
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
    async getImages(callback) {
        var conn = db.getConnection();
        conn.connect(function (err) {
            if (err) {
                //console.log(err);
                return callback(err,null);
            }
            else {
                var sql = 'SELECT productId, name, path FROM SP_AIR.product';
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
    async getImage(productId, callback) {
        var conn = db.getConnection();
        conn.connect(function (err) {
            if (err) {
                //console.log(err);
                return callback(err,null);
            }
            else {
                var sql = 'SELECT productId, name, path FROM SP_AIR.product WHERE productId=?';
                conn.query(sql, [productId], function (err, result) {
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

module.exports = product;