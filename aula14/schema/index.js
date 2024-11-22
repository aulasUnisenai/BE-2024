const { gql } = require('apollo-server-express');

const typeDefs = gql`
    type Produto {
        id: ID!
        nome: String!
        categoria: String!
        quantidade: Int!
        preco: Float!
    }

    type Query {
        listarProdutos: [Produto!]!
        buscarProduto(id: ID!): Produto
    }

    type Mutation {
        adicionarProduto(nome: String!, categoria: String!, quantidade: Int!, preco: Float!): Produto
        atualizarProduto(id: ID!, nome: String, categoria: String, quantidade: Int, preco: Float): Produto
        removerProduto(id: ID!): String
    }
`;

module.exports = typeDefs;