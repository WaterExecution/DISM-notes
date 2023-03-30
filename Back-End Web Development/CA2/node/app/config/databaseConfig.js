const { Sequelize } = require('sequelize');

sql_username = "root"
sql_password = "password"
database = "SP_AIR"

const sequelize = new Sequelize(database, sql_username, sql_password, {
  host: 'localhost',
  dialect: 'mysql',
  logging: false,
});

module.exports = sequelize;


// var mysql=require('mysql2');

// var dbConnect={
    // getConnection:function(){
        // var conn=mysql.createConnection({
            // host:"127.0.0.1",
            // user:"root",
            // password:"password",
            // database:"SP_AIR"
        // });
        // return conn;
    // }
// }
// module.exports=dbConnect;
