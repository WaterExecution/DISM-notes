CREATE DATABASE IF NOT EXISTS `SP_AIR`;
USE `SP_AIR`;
DROP TABLE IF EXISTS `booking`;
DROP TABLE IF EXISTS `flights`;
DROP TABLE IF EXISTS `airports`;
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`(
  userid INT AUTO_INCREMENT NOT NULL,
  username varchar(255) UNIQUE NOT NULL,
  email varchar(255) UNIQUE NOT NULL,
  contact varchar(255),
  password varchar(255) NOT NULL,
  role varchar(255) NOT NULL,
  profile_pic_url varchar(512) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  PRIMARY KEY (userid)
);
CREATE TABLE `airports`(
  airportid INT AUTO_INCREMENT NOT NULL,
  name varchar(255) UNIQUE NOT NULL,
  country varchar(255) NOT NULL,
  description varchar(10000),
  PRIMARY KEY (airportid)
);
CREATE TABLE `flights`(
  flightId INT AUTO_INCREMENT NOT NULL,
  flightCode varchar(255) NOT NULL,
  aircraft varchar(255) NOT NULL,
  originAirport INT NOT NULL,
  destinationAirport INT NOT NULL,
  embarkDate varchar(255) NOT NULL,
  travelTime varchar(255) NOT NULL,
  price decimal(10,2) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  PRIMARY KEY (flightId),
  FOREIGN KEY (originAirport) REFERENCES airports(airportId) ON DELETE CASCADE,
  FOREIGN KEY (destinationAirport) REFERENCES airports(airportId) ON DELETE CASCADE
);
CREATE TABLE `booking`(
  bookingId INT AUTO_INCREMENT NOT NULL,
  name varchar(255) NOT NULL,
  passport varchar(255) NOT NULL,
  nationality varchar(255) NOT NULL,
  age INT NOT NULL,
  fk_userId INT NOT NULL,
  fk_flightId INT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  PRIMARY KEY (bookingId),
  FOREIGN KEY (fk_userId) REFERENCES SP_AIR.users(userId) ON DELETE CASCADE,
  FOREIGN KEY (fk_flightId) REFERENCES SP_AIR.flights(flightId) ON DELETE CASCADE
);

insert into sp_air.airports (name, country, description) values ("Singapore Airport", "Singapore", "Singapore");
insert into sp_air.airports (name, country, description) values ("Malaysia Airport", "Malaysia", "Malaysia");
insert into sp_air.airports (name, country, description) values ("Japan Airport", "Japan", "Japan");
insert into sp_air.flights (flightCode, aircraft, originAirport, destinationAirport, embarkDate, travelTime, price) values ("SP123", "Air123", "1", "2", "2022-12-30 10:24", "2 Hours", "300");
insert into sp_air.flights (flightCode, aircraft, originAirport, destinationAirport, embarkDate, travelTime, price) values ("SP123", "Air123", "2", "3", "2022-12-31 10:24", "5 Hours", "600");
insert into sp_air.flights (flightCode, aircraft, originAirport, destinationAirport, embarkDate, travelTime, price) values ("SP123", "Air123", "1", "2", "2022-07-01 10:23", "2 Hours", "300");
insert into sp_air.flights (flightCode, aircraft, originAirport, destinationAirport, embarkDate, travelTime, price) values ("SP123", "Air123", "2", "3", "2022-08-31 10:24", "5 Hours", "600");
insert into sp_air.flights (flightCode, aircraft, originAirport, destinationAirport, embarkDate, travelTime, price) values ("SP123", "Air123", "2", "1", "2022-12-31 10:24", "2 Hours", "300");
insert into sp_air.users (username, email, contact, password, role, profile_pic_url) values ("customer", "customer@dismairlines.com", "97654321", "$2b$10$zzMsXn4G31TSkvEgl7Acb.oteSy0iZQAusQBkvNk8vVbzlgi.8RuS", "Customer", "somewhere");
insert into sp_air.users (username, email, contact, password, role, profile_pic_url) values ("admin", "admin@dismairlines.com", "87654321", "$2b$10$zzMsXn4G31TSkvEgl7Acb.oteSy0iZQAusQBkvNk8vVbzlgi.8RuS", "Admin", "somewhere");