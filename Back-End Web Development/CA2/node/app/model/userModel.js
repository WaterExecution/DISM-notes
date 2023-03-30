const { Sequelize, DataTypes } = require("sequelize");
const sequelize = require("../config/databaseConfig.js");

const User = sequelize.define(
    "users",
    {
        userid: {
            type: DataTypes.INTEGER,
            autoIncrement: true,
            allowNull: false,
            primaryKey: true,
        },
        username: {
            type: DataTypes.STRING,
            allowNull: false,
        },
        email: {
            type: DataTypes.STRING,
            allowNull: false,
			validate: {
				isEmail: true,
			},
        },
        contact: {
            type: DataTypes.STRING,
			defaultValue: "",
            allowNull: true,
        },
        password: {
            type: DataTypes.STRING,
            allowNull: false,
        },
        role: {
            type: DataTypes.STRING,
            allowNull: false,
        },
        profile_pic_url: {
            type: DataTypes.STRING,
			defaultValue: "./img/default.jpg",
            allowNull: true,
        },
    },
    {
        timestamps: false,
    }
);

module.exports = User;