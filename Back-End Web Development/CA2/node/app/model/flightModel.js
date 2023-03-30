const { Sequelize, DataTypes } = require("sequelize");
const sequelize = require("../config/databaseConfig.js");

const Flight = sequelize.define(
    "flights",
    {
        flightid: {
            type: DataTypes.INTEGER,
            autoIncrement: true,
            allowNull: false,
            primaryKey: true,
        },
        flightCode: {
            type: DataTypes.STRING,
            allowNull: false,
        },
        aircraft: {
            type: DataTypes.STRING,
            allowNull: false,
        },
        originAirport: {
            type: DataTypes.STRING,
            allowNull: false,
        },
		destinationAirport: {
            type: DataTypes.STRING,
            allowNull: false,
        },
        embarkDate: {
            type: DataTypes.STRING,
            allowNull: false,
        },
		travelTime: {
            type: DataTypes.STRING,
            allowNull: false,
        },
		price: {
            type: DataTypes.STRING,
            allowNull: false,
        },
    },
    {
        timestamps: false,
    }
);

module.exports = Flight;