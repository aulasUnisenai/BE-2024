const musicaModelo = require('../models/musicaModelo');

const resolvers = {
    Query: {
        recomendacoes: (_, args) => musicaModelo.obterRecomendacoes(args),
        generosDisponiveis: () => musicaModelo.obterGenerosDisponiveis(),
        humoresDisponiveis: () => musicaModelo.obterHumoresDisponiveis(),
    },
};

module.exports = resolvers;
