// Bibliotecas
const express = require('express');
const mongoose = require('mongoose');
const {ObjectId} = require('mongodb');
const multer = require('multer');
const upload = multer();
const app = express();

// Configurações
app.use(express.json());

// Carregar o arquivo config.js
const config = require('./config.json');

// Configurar credenciais
const usuario = encodeURIComponent(config.usuario); 
const senha = encodeURIComponent(config.senha);
const uri = `mongodb+srv://${usuario}:${senha}@cluster1.tjqkv.mongodb.net/?retryWrites=true&w=majority&appName=cluster1`;

// Conectar ao MongoDB
mongoose.connect(uri).then(() =>
    console.log('Conectado ao MongoDB')
).catch((err) => 
    console.error('Erro ao conectar ao MongoDB', err)
);

// Definir o schema do banco
const musicSchema = new mongoose.Schema({
    titulo: {type: String, required: true},
    artista: {type: String, required: true},
    genero: {type: String, required: true},
    ano_lancamento: {type: Number, required: true},
    faixas: {type: [String], required: true}, // Array de strings
});

// Criar coleção com base no schema
const ColecaoMusicas = mongoose.model('musicas', musicSchema);

// Rota para enviar o json
app.post('/enviar_json', upload.single('arquivo'), async(req, res) => {
    const {file} = req;
    if(!file || !file.originalname) {
        return res.status(400).json({erro: "Nenhum arquivo selecionado ou enviado"});
    }
    try {
        const dados = JSON.parse(file.buffer.toString());
        if(Array.isArray(dados)) {
            await ColecaoMusicas.insertMany(dados);
        } else {
            await ColecaoMusicas.insertOne(dados);
        }
        res.status(200).json({mensagem: "Dados JSON inseridos com sucesso."});
    } catch(erro) {
        res.status(400).json({erro: `Erro ao processar o arquivo:${erro}`});
    }
});

// Rota para consultar 
app.get('/consultar_json', async(req,res) => {
    try {
        // Verificar se um ID foi fornecido
        const {id} = req.query;

        if(id) {
            if(!ObjectId.isValid(id)) {
                return res.status(400).json({erro: "ID inválido"});
            }
            const documento = await ColecaoMusicas.findById(id);
            if (!documento) {
                return res.status(404).json({erro: "Documento não encontrado"});
            }
            res.status(200).json(documento);
        } else {
            // Se nenhum ID for fornecido, retorna todos os documentos
            const documentos = await ColecaoMusicas.find({});
            res.status(200).json(documentos);
        }
    } catch(erro) {
        res.status(500).json({erro: erro.message});
    }
});

// Rota para atualizar
app.put('/atualizar_json', async(req, res) => {
    try {
        const {id} = req.query;
        let criterio = {};

        if(id) {
            if (!ObjectId.isValid(id)) {
                return res.status(400).json({erro: "ID inválido."});
            }
            criterio._id = new ObjectId(id);
        } else {
            criterio = req.body.criterio || {};
        }

        const dadosAtualizados = req.body.dados_atualizados;
        if (!dadosAtualizados) {
            return res.status(400).json({erro: "Nenhum dado fornecido para atualização"});
        }

        const resultado = await ColecaoMusicas.updateMany(criterio, {$set: dadosAtualizados});

        if(resultado.matchedCount === 0) {
            return res.status(404).json({erro: "Nenhum documento encontrado com os critérios fornecidos!"});
        }

        res.status(200).json({
            mensagem: "Documentos atualizados com sucesso.",
            documentos_atualizados: resultado.modifiedCount
        });
    } catch(erro) {
        res.status(500).json({erro: erro.message});
    }
});

// Rota para deletar
app.delete('/deletar_json', async(req, res) => {
    try {
        const {id} = req.query;
        let criterio = {};

        if(id) {
            if(!ObjectId.isValid(id)) {
                return res.status(400).json({erro: "Id inválido!"});
            }
            criterio._id = new ObjectId(id);
        } else {
            criterio = req.body.criterio || {};
        }

        const resultado = await ColecaoMusicas.deleteMany(criterio);

        if (resultado.deletedCount ===0) {
            return res.status(404).json({erro: "Nenhum documento encontrado com os critérios fornecidos"});
        }

        res.status(200).json({
            mensagem: "Documentos deletados com sucesso!",
            documentos_deletados: resultado.deletedCount
        });
    } catch(erro) {
        res.status(500).json({erro: erro.message});
    }
});

// Iniciar a aplicação
const porta = 3000;
app.listen(porta, () => {
    console.log(`Servidor rodando em http://localhost:${porta}`);
});