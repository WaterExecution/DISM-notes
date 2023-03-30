const { Sequelize, DataTypes } = require("sequelize");
const sequelize = require("../config/databaseConfig.js");

const Booking = sequelize.define(
    "booking",
    {
        bookingid: {
            type: DataTypes.INTEGER,
            autoIncrement: true,
            allowNull: false,
            primaryKey: true,
        },
        name: {
            type: DataTypes.STRING,
            allowNull: false,
        },
        passport: {
            type: DataTypes.STRING,
            allowNull: false,
        },
        nationality: {
            type: DataTypes.STRING,
            allowNull: false,
        },
        age: {
            type: DataTypes.STRING,
            allowNull: false,
        },
        fk_userid: {
            type: DataTypes.STRING,
            allowNull: false,
        },
        fk_flightid: {
            type: DataTypes.STRING,
            allowNull: true,
        },
    },
    {
        timestamps: false,
		freezeTableName: true,
    }
);

module.exports = Booking;