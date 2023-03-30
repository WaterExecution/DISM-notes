/*
/////////////////////////////////
// Name: Tong Yew Ching Kelvin //
// Admission: 2136871          //
// Class: DISM/FT/2B/21        //
/////////////////////////////////
*/

CREATE DATABASE IF NOT EXISTS `SP_AIR`;
USE `SP_AIR`;
DROP TABLE IF EXISTS `booking`;
DROP TABLE IF EXISTS `flight`;
DROP TABLE IF EXISTS `airport`;
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`(
  userId INT AUTO_INCREMENT NOT NULL,
  username varchar(255) UNIQUE NOT NULL,
  email varchar(255) UNIQUE NOT NULL,
  contact varchar(255) NOT NULL,
  password varchar(255) NOT NULL,
  role varchar(255) NOT NULL,
  profile_pic_url varchar(512) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  PRIMARY KEY (userId)
);
CREATE TABLE `airport`(
  airportId INT AUTO_INCREMENT NOT NULL,
  name varchar(255) UNIQUE NOT NULL,
  country varchar(255) NOT NULL,
  description varchar(10000) NOT NULL,
  PRIMARY KEY (airportId)
);
CREATE TABLE `flight`(
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
  FOREIGN KEY (originAirport) REFERENCES airport(airportId) ON DELETE CASCADE,
  FOREIGN KEY (destinationAirport) REFERENCES airport(airportId) ON DELETE CASCADE
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
  FOREIGN KEY (fk_userId) REFERENCES SP_AIR.user(userId) ON DELETE CASCADE,
  FOREIGN KEY (fk_flightId) REFERENCES SP_AIR.flight(flightId) ON DELETE CASCADE
);
CREATE TABLE `product`(
  productId INT AUTO_INCREMENT NOT NULL,
  name varchar(255) NOT NULL,
  path varchar(255) NOT NULL,
  PRIMARY KEY (productId)
);