import sqlite3


def database():
    connection = sqlite3.connect("attendance.db")
    cursor = connection.cursor()
    cursor.execute('''DROP TABLE IF EXISTS `attendance`;''')
    cursor.execute('''CREATE TABLE `attendance` (
  `attendanceid` INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
  `studentid` INTEGER NOT NULL,
  `lessonid` INTEGER NOT NULL,
  `present` varchar(1),
  CONSTRAINT `lessionid` FOREIGN KEY (`lessonid`) REFERENCES `lesson` (`lessonid`),
  CONSTRAINT `studentid` FOREIGN KEY (`studentid`) REFERENCES `students` (`studentid`)
  );''')
    cursor.execute('''DROP TABLE IF EXISTS `class`;''')
    cursor.execute('''CREATE TABLE `class` (
  `classid` INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
  `name` varchar(255) NOT NULL
  );''')
    cursor.execute('''DROP TABLE IF EXISTS `enrollment`;''')
    cursor.execute('''CREATE TABLE `enrollment` (
  `enrollmentid` INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
  `studentid` INTEGER NOT NULL,
  `classid` INTEGER NOT NULL,
  CONSTRAINT `studentid` FOREIGN KEY (`studentid`) REFERENCES `student` (`studentid`)
  CONSTRAINT `classid` FOREIGN KEY (`classid`) REFERENCES `class` (`classid`)
  );''')
    cursor.execute('''DROP TABLE IF EXISTS `lesson`;''')
    cursor.execute('''CREATE TABLE `lesson` (
  `lessonid` INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
  `classid` INTEGER NOT NULL,
  `date` time NOT NULL,
  `classroom` varchar(255) NOT NULL,
  `timespan` varchar(255) NOT NULL,
  CONSTRAINT `classid` FOREIGN KEY (`classid`) REFERENCES `class` (`classid`)
);''')
    cursor.execute('''DROP TABLE IF EXISTS `students`;''')
    cursor.execute('''CREATE TABLE `students` (
  `studentid` INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
  `uid` varchar(255) NOT NULL UNIQUE,
  `firstname` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `rfid` varchar(255) NOT NULL UNIQUE
  );''')
    cursor.close()
    connection.commit()
    connection.close()
    return


def thingspeak():
    return


database()
conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()
cursor.execute(
    "insert into students (`uid`,`firstname`,`lastname`,`rfid`) VALUES('1234567','elmo','muppet','426378240664')"
)
cursor.execute(
    "insert into students (`uid`,`firstname`,`lastname`,`rfid`) VALUES('1234568','big','bird','357793243804')"
)
cursor.execute(
    "insert into students (`uid`,`firstname`,`lastname`,`rfid`) VALUES('1234569','count','von count','15503399831')"
)
cursor.execute(
    "insert into students (`uid`,`firstname`,`lastname`,`rfid`) VALUES('1234570','cookie','monster','358027827979')"
)
cursor.execute(
    "insert into students (`uid`,`firstname`,`lastname`,`rfid`) VALUES('1234571','kermit','frog','856987433526')"
)
cursor.execute(
    "insert into students (`uid`,`firstname`,`lastname`,`rfid`) VALUES('1234572','ernie','muppet','85456433526')"
)
cursor.execute(
    "insert into students (`uid`,`firstname`,`lastname`,`rfid`) VALUES('1234573','bert','muppet','85123433526')"
)
cursor.execute(
    "insert into class ('name') values ('PYTHON PROGRAMMING FOR IOT')")
cursor.execute("insert into class ('name') values ('AI ESSENTIALS')")
cursor.execute("insert into class ('name') values ('CREATING AN IOT PROJECT')")
cursor.execute(
    "insert into class ('name') values ('LOW-CODE AI APPLICATIONS')")
cursor.execute("insert into class ('name') values ('ACCOUNTING')")
#lesson
cursor.execute("insert into lesson values ('1','1','2022-12-15 08:00','T1111','1 hours')")
cursor.execute("insert into lesson values ('2','1','2022-12-22 08:00','T1111','1 hours')")
cursor.execute("insert into lesson values ('3','2','2022-12-15 08:00','T1122','1 hours')")
cursor.execute("insert into lesson values ('4','2','2022-12-22 08:00','T1122','1 hours')")
cursor.execute("insert into lesson values ('5','3','2022-12-15 08:00','T1133','1 hours')")
cursor.execute("insert into lesson values ('6','3','2022-12-22 08:00','T1133','1 hours')")
cursor.execute("insert into lesson values ('7','4','2022-12-15 08:00','T1144','1 hours')")
cursor.execute("insert into lesson values ('8','4','2022-12-22 08:00','T1144','1 hours')")
cursor.execute("insert into lesson values ('9','5','2022-12-15 08:00','T1155','1 hours')")
cursor.execute("insert into lesson values ('10','5','2022-12-22 08:00','T1155','1 hours')")
#enrollment
cursor.execute(
    "insert into enrollment ('enrollmentid','studentid','classid') values ('1','1','1')"
)
cursor.execute(
    "insert into enrollment ('enrollmentid','studentid','classid') values ('2','2','1')"
)
cursor.execute(
    "insert into enrollment ('enrollmentid','studentid','classid') values ('3','3','1')"
)
cursor.execute(
    "insert into enrollment ('enrollmentid','studentid','classid') values ('4','4','1')"
)
cursor.execute(
    "insert into enrollment ('enrollmentid','studentid','classid') values ('5','1','2')"
)
cursor.execute(
    "insert into enrollment ('enrollmentid','studentid','classid') values ('6','5','2')"
)
cursor.execute(
    "insert into enrollment ('enrollmentid','studentid','classid') values ('7','6','2')"
)
cursor.execute(
    "insert into enrollment ('enrollmentid','studentid','classid') values ('8','7','2')"
)
cursor.execute(
    "insert into enrollment ('enrollmentid','studentid','classid') values ('9','2','3')"
)
cursor.execute(
    "insert into enrollment ('enrollmentid','studentid','classid') values ('10','4','3')"
)
cursor.execute(
    "insert into enrollment ('enrollmentid','studentid','classid') values ('11','6','3')"
)
cursor.execute(
    "insert into enrollment ('enrollmentid','studentid','classid') values ('12','7','3')"
)
cursor.execute(
    "insert into enrollment ('enrollmentid','studentid','classid') values ('13','1','4')"
)
cursor.execute(
    "insert into enrollment ('enrollmentid','studentid','classid') values ('14','3','4')"
)
cursor.execute(
    "insert into enrollment ('enrollmentid','studentid','classid') values ('15','5','4')"
)
cursor.execute(
    "insert into enrollment ('enrollmentid','studentid','classid') values ('16','7','4')"
)
cursor.execute(
    "insert into enrollment ('enrollmentid','studentid','classid') values ('17','1','5')"
)
cursor.execute(
    "insert into enrollment ('enrollmentid','studentid','classid') values ('18','4','5')"
)
cursor.execute(
    "insert into enrollment ('enrollmentid','studentid','classid') values ('19','6','5')"
)
cursor.execute(
    "insert into enrollment ('enrollmentid','studentid','classid') values ('20','7','5')"
)

#attendance
cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('1','1','1','P')"
)
cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('2','2','1','P')"
)
cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('3','3','1','P')"
)
cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('4','4','1','A')"
)
cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('5','1','2','P')"
)
cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('6','2','2','P')"
)
cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('7','3','2','A')"
)
cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('8','4','2','A')"
)
cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('9','1','3','P')"
)

cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('10','5','3','A')"
)

cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('11','6','3','P')"
)

cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('12','7','3','P')"
)

cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('13','1','4','P')"
)

cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('14','5','4','P')"
)

cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('15','6','4','A')"
)

cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('16','7','4','P')"
)

cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('17','2','5','P')"
)

cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('18','4','5','P')"
)

cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('19','6','5','P')"
)

cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('20','7','5','P')"
)

cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('21','2','6','A')"
)

cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('22','4','6','')"
)

cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('23','6','6','P')"
)

cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('24','7','6','P')"
)

cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('25','1','7','A')"
)

cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('26','3','7','P')"
)

cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('27','5','7','P')"
)

cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('28','7','7','P')"
)

cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('29','1','8','P')"
)

cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('30','3','8','A')"
)

cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('31','5','8','P')"
)

cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('32','7','8','P')"
)

cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('33','1','9','A')"
)

cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('34','4','9','A')"
)

cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('35','6','9','P')"
)

cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('36','7','9','P')"
)

cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('37','1','10','P')"
)

cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('38','4','10','A')"
)

cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('39','6','10','P')"
)

cursor.execute(
    "insert into attendance ('attendanceid','studentid','lessonid','present') values ('40','7','10','A')"
)
 
cursor.close()
conn.commit()
conn.close()
