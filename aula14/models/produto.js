// Importar o módulo fs (filesystem) para leitura e escrita de arquivos
const fs = require('fs');

// Importar o módulo path para resolver o caminho do arquivo
const path = require('path');

// Caminho do arquivo JSON onde os produtos são armazenados
const caminhoArquivo = path.resolve('data', 'produtos.json');

// Função para ler os produtos do arquivo JSON
const lerProdutos = () => {
    // Ler o arquivo de forma síncrona
    const dados = fs.readFileSync(caminhoArquivo, 'utf-8');
    
    // Parsear o conteúdo do arquivo JSON para um objeto JavaScript
    return JSON.parse(dados);
};

// Função para salvar a lista de produtos no arquivo JSON
const salvarProdutos = (produtos) => {
    // Converter o array de produtos em uma string JSON e escrevendo no arquivo de forma síncrona
    fs.writeFileSync(caminhoArquivo, JSON.stringify(produtos, null, 2));
};

// Exportar as funções lerProdutos e salvarProdutos para que possam ser usadas em outros arquivos
module.exports = { lerProdutos, salvarProdutos };