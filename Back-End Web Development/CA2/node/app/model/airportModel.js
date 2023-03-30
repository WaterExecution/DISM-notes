const { Sequelize, DataTypes } = require("sequelize");
const sequelize = require("../config/databaseConfig.js");

const Airport = sequelize.define(
    "airports",
    {
        airportId: {
            type: DataTypes.INTEGER,
            autoIncrement: true,
            allowNull: false,
            primaryKey: true,
        },
        name: {
            type: DataTypes.STRING,
            allowNull: false,
        },
        country: {
            type: DataTypes.STRING,
            allowNull: false,
        },
        description: {
            type: DataTypes.STRING(1024),
            allowNull: true,
        },
    },
    {
        timestamps: false,
    }
);

module.exports = Airport;