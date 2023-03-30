const multer = require("multer")

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, './uploads')  //update according to OS
  },
  filename: function (req, file, cb) {
    cb(null, "image-"+Date.now())
  }
})
 
const upload = multer({ storage: storage })

module.exports = upload

