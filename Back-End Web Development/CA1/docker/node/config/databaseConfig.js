var mysql=require('mysql2');

var dbConnect={
    getConnection:function(){
        var conn=mysql.createConnection({
            host:"db",
            user:"root",
            password:"password",
            database:"SP_AIR"
        });
        return conn;
    }
}
module.exports=dbConnect;

/////////////////////////////////
// Name: Tong Yew Ching Kelvin //
// Admission: 2136871          //
// Class: DISM/FT/2B/21        //
/////////////////////////////////