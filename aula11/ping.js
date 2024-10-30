// Bibliotecas
const express = require('express');
const mongoose = require('mongoose');
const app = express();

// Escape o nome do usuário e a senha
const usuario = encodeURIComponent('seuUsuario');
const senha = encodeURIComponent('suaSenha');

// URI de conexão
const uri = `suaURI + usuario + senha`;

//Função para conectar ao MongoDB
async function conectarMongoDB() {
    try {
        await mongoose.connect(uri);
        console.log('Sucesso ao conectar ao MongoDB');
        return true;
    } catch(erro) {
        console.error('Erro ao conectar ao MongoDB:', erro);
        return false;
    }
}

// Rota para testar a conexão
app.get('/ping', async(req, res) => {
    const conectado = await conectarMongoDB();
    if(conectado) {
        res.send('Sucesso ao conectar ao MongoDB');
    } else {
        res.status(500).send('Erro ao conectar ao MongoDB');
    }

    // Fechar a conexão
    mongoose.connection.close();
});

// Iniciar a aplicação
const porta = 3000;
app.listen(porta, () => {
    console.log(`Servidor rodando em http://localhost:${porta}`);
});
