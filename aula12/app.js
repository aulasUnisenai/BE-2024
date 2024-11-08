import express from "express";
import axios from 'axios';
import dotenv from 'dotenv';
import {cliente, conectarRedis} from './redisClient.js';
import sequelize from './db.js';
import Clima from './clima.js';

dotenv.config();

const app = express();
const PORTA = process.env.PORTA || 3000;

// Conectar ao Redis e ao banco de dados
conectarRedis();
sequelize.sync();

// Rota para buscar clima
app.get('/clima/:cidade', async(req, res) => {
    const cidade = req.params.cidade; 

    // Tentar buscar os dados do cache
    try {
        const dadosCache = await cliente.get(cidade);
        if (dadosCache) {
            return res.json(JSON.parse(dadosCache));
        }
    } catch(error) {
        console.error('Erro ao acessor o cache:', error);
    }

    // Se não estiver no cache, requisitar à API
    const apiKey = process.env.OPENWEATHER_API_KEY;
    try {
        const resposta = await axios.get(`https://api.openweathermap.org/data/2.5/weather?q=${cidade}&appid=${apiKey}&lang=pt_br&units=metric`);
        const dadosClima = {
            cidade: resposta.data.name,
            temperatura: resposta.data.main.temp,
            descricao: resposta.data.weather[0].description
        };

        // Armazenar no banco de dados
        await Clima.create(dadosClima);

        // Armazenar no cache (Redis)
        await cliente.setEx(cidade, 3600, JSON.stringify(dadosClima));

        res.json(dadosClima);
    } catch(error) {
        console.error('Erro ao buscar dados de clima:', error);
        res.status(500).json({message: 'Erro ao buscar dados do clima', error: error.message});
    }
});

// Iniciar a aplicação
app.listen(PORTA, () => {
    console.log(`Servidor rodando em: http://localhost:${PORTA}`);
});
