const fs = require('fs');
const path = require('path');

let musicas = [];

// Carregar dados do arquivo JSON
const carregarMusicas = () => {
    const caminhoArquivo = path.join(__dirname, '../data/musicas.json');
    const dados = fs.readFileSync(caminhoArquivo, 'utf-8');
    musicas = JSON.parse(dados);
};

// Funções para obter recomendações
const obterRecomendacoes = ({genero, humor}) =>
    musicas.filter(musica => 
    (!genero || musica.genero === genero) &&
    (!humor || musica.humor === humor)
    );

// Funções para listar os gêneros e humores
const obterGenerosDisponiveis = () => [... new Set(musicas.map(musica => musica.genero))];
const obterHumoresDisponiveis = () => [... new Set(musicas.map(musica => musica.humor))];

// Carregar as músicas ao iniciar o modelo
carregarMusicas();

module.exports = {
    obterRecomendacoes,
    obterGenerosDisponiveis,
    obterHumoresDisponiveis,
};
