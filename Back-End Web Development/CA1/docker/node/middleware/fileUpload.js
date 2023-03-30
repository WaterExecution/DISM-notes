const multer = require("multer")

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, '/usr/app/uploads')  //update according to OS
  },
  filename: function (req, file, cb) {
    cb(null, "image-"+Date.now())
  }
})
 
const upload = multer({ storage: storage })

module.exports = upload



/////////////////////////////////
// Name: Tong Yew Ching Kelvin //
// Admission: 2136871          //
// Class: DISM/FT/2B/21        //
/////////////////////////////////