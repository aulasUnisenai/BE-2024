import { DataTypes } from "sequelize";
import sequelize from './db.js';

const Clima = sequelize.define('Clima',  {
    cidade: {
        type: DataTypes.STRING,
        allowNull: false
    },
    temperatura: {
        type:DataTypes.FLOAT,
        allowNull: false
    },
    descricao: {
        type: DataTypes.STRING,
        allowNull: false
    }
}, {
    timestamps: true,
});

export default Clima;
