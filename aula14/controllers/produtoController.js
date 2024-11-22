// Importar as funções para manipular os produtos no arquivo JSON
const { lerProdutos, salvarProdutos } = require('../models/produto');

const resolvers = {
    // Definir os resolvers para as consultas (queries) GraphQL
    Query: {
        // Resolver para listar todos os produtos
        listarProdutos: () => lerProdutos(), // Retorna todos os produtos do arquivo JSON

        // Resolver para buscar um produto específico pelo ID
        buscarProduto: (_, { id }) => {
            const produtos = lerProdutos(); // Lê todos os produtos
            return produtos.find((produto) => produto.id === id); // Busca e retorna o produto com o ID fornecido
        }
    },

    // Definir os resolvers para as mutações (modificações de dados) GraphQL
    Mutation: {
        // Adicionar um novo produto ao estoque
        adicionarProduto: (_, { nome, categoria, quantidade, preco }) => {
            const produtos = lerProdutos(); // Lê todos os produtos existentes
            const novoProduto = {
                id: String(produtos.length + 1), // Gera um ID único baseado no tamanho do array
                nome,
                categoria,
                quantidade,
                preco
            };
            produtos.push(novoProduto); // Adiciona o novo produto ao array
            salvarProdutos(produtos); // Salva o array atualizado no arquivo JSON
            return novoProduto; // Retorna o produto recém-criado
        },

        // Atualizar os dados de um produto existente
        atualizarProduto: (_, { id, nome, categoria, quantidade, preco }) => {
            const produtos = lerProdutos(); // Lê todos os produtos existentes
            const produto = produtos.find((p) => p.id === id); // Encontra o produto pelo ID
            if (!produto) throw new Error('Produto não encontrado'); // Retorna erro se o produto não existir

            // Atualizar os campos do produto, se fornecidos
            if (nome) produto.nome = nome;
            if (categoria) produto.categoria = categoria;
            if (quantidade !== undefined) produto.quantidade = quantidade;
            if (preco !== undefined) produto.preco = preco;

            salvarProdutos(produtos); // Salva o array atualizado no arquivo JSON
            return produto; // Retorna o produto atualizado
        },

        // Remover um produto do estoque
        removerProduto: (_, { id }) => {
            const produtos = lerProdutos(); // Lê todos os produtos existentes
            const indice = produtos.findIndex((produto) => produto.id === id); // Encontra o índice do produto pelo ID
            if (indice === -1) throw new Error('Produto não encontrado'); // Retorna erro se o produto não existir

            produtos.splice(indice, 1); // Remove o produto do array
            salvarProdutos(produtos); // Salva o array atualizado no arquivo JSON
            return 'Produto removido com sucesso'; // Retorna mensagem de sucesso
        }
    }
};

// Exportar os resolvers para serem usados no servidor Apollo
module.exports = resolvers;