import express from "express";
import {cliente, conectarRedis} from './redisClient.js';

const app = express();

// Conectar ao Redis
conectarRedis();

// Rota para o ping
app.get('/ping', async(req, res) => {
    try {
        const resposta = await cliente.ping();
        res.json({mensagem: "Redis está funcionando!", resposta});
    } catch(error) {
        console.error("Erro ao conectar ao Redis:", error);
        res.status(500).json({mensagem: "Erro ao conectar ao Redis:", error});
    }
});

// Iniciar o servidor
const PORTA = process.env.PORTA || 3000;
app.listen(PORTA, () => {
    console.log(`Servidor rodando em: http://localhost:${PORTA}`)
});
