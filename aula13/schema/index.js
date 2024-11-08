const {gql} = require('apollo-server-express');

const typeDefs = gql`
    type Musica {
        titulo: String!
        artista: String!
        genero: String!
        humor: String!
    }
    
    type Query {
        recomendacoes(genero: String, humor: String): [Musica]
        generosDisponiveis: [String]
        humoresDisponiveis: [String]
    }
`;

module.exports = typeDefs;
