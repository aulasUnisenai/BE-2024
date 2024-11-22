// Bibliotecas e módulos
const express = require('express');
const { ApolloServer } = require('apollo-server-express');
const typeDefs = require('./schema');
const resolvers = require('./controllers/produtoController');

// Iniciar a aplicação
const iniciarServidor = async () => {
    const app = express();
    const servidor = new ApolloServer({ typeDefs, resolvers });
    await servidor.start();
    servidor.applyMiddleware({ app });

    app.listen(4000, () => {
        console.log(`Servidor rodando em: http://localhost:4000${servidor.graphqlPath}`);
    });
};

iniciarServidor();
