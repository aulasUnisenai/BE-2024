import { Sequelize } from "sequelize";
import dotenv from "dotenv";

dotenv.config();

const sequelize = new Sequelize(process.env.DB_NOME, process.env.DB_USUARIO, process.env.DB_SENHA, {
    host: process.env.DB_HOST,
    dialect:'mariadb'
});

export default sequelize;
