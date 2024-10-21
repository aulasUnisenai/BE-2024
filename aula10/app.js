// Bibliotecas
const express = require('express');
const {Sequelize, Datatypes, DataTypes} = require('sequelize');
const bodyParser = require('body-parser');
const path = require('path');
const expressLayouts = require('express-ejs-layouts');
const { title } = require('process');

// Configurações
const app = express();
const PORTA = 3000;
const DB_NAME = 'academico';

// Middleware para usar o express-ejs-layouts
app.use(expressLayouts);

// Configurar o EJS como motor de templates
app.set('view engine', 'ejs');

// Diretório das views
app.set('views', path.join(__dirname, 'views'));

// Configuração do layout padrão
app.set('layout', 'base');

// Middleware para as requisições
app.use(bodyParser.urlencoded({extended: false}));

// Configuração do banco de dados
const sequelize = new Sequelize(DB_NAME, 'root', '1234', {
    host: 'localhost',
    dialect: 'mariadb',
    logging: false,
});

// Definição do modelo Disciplina
const Disciplina = sequelize.define('Disciplina', {
    nome: {
        type: DataTypes.STRING,
        allowNull: false,
    },
    carga_horaria: {
        type: DataTypes.INTEGER,
        allowNull: false,
    },
    professor: {
        type:DataTypes.STRING,
        allowNull: false,
    },
});

// Sincronizar o banco de dados e criar a tabela
async function startApp() {
    try {
        await sequelize.sync(); // Sicronizar com o banco
        console.log('Banco de dados sincronizado com sucesso.');
    
        // Inicializar a aplicação
        app.listen(PORTA, () => {
           console.log(`Servidor rodando em http://localhost:${PORTA}`); 
        });
    } catch(error) {
        console.error('Erro ao sincronizar o banco de dados:', error);
    }
}

// Chamar a função para iniciar o app
startApp();

// Rota principal
app.get('/', async (req, res) => {
    const disciplinas = await Disciplina.findAll();
    res.render('index', {disciplinas});
});

// Rota para exibir o formulário de adição de uma disciplina
app.get('/add', (req, res) => {
    res.render('edit', {disciplina: null, title: 'Adicionar Disciplina'});
});

// Rota para processar o formulário de adição ou edição
app.post('/add', async(req, res) => {
    const {id, nome, carga_horaria, professor} = req.body;
    try {
        if (id) {
            const disciplina = await Disciplina.findByPk(id);
            if (!disciplina) {
                return res.status(404).send('Disciplina não encontrada');
            }
            disciplina.nome = nome;
            disciplina.carga_horaria = parseInt(carga_horaria);
            disciplina.professor = professor;
            await disciplina.save();
        } else {
            await Disciplina.create({nome, carga_horaria, professor});
        }
        res.redirect('/');
    } catch(error) {
        res.status(500).send('Erro ao salvar a disciplina');
    }
});

// Rota para exibir o formulário de edição
app.get('/edit/:id', async(req, res) => {
    const disciplina = await Disciplina.findByPk(req.params.id);
    if (!disciplina) {
        return res.status(404).send('Disciplina não encontrada.');
    }
    res.render('edit',{disciplina, title:'Editar disciplina'});
});

// Rota para exibir a confirmação de exclusão de uma disciplina
app.get('/delete/:id', async (req, res) => {
    const disciplina = await Disciplina.findByPk(req.params.id); // Busca a disciplina pelo ID fornecido na URL
    if (!disciplina) {
        return res.status(404).send('Disciplina não encontrada'); // Retorna erro se a disciplina não for encontrada
    }
    res.render('delete', { disciplina, title: 'Excluir Disciplina' }); // Renderiza a página de confirmação de exclusão
});

// Rota para processar a exclusão de uma disciplina
app.post('/delete/:id', async (req, res) => {
    const disciplina = await Disciplina.findByPk(req.params.id); // Busca a disciplina pelo ID fornecido na URL
    if (!disciplina) {
        return res.status(404).send('Disciplina não encontrada'); // Retorna erro se a disciplina não for encontrada
    }
    try {
        await disciplina.destroy(); // Remove a disciplina do banco de dados
        res.redirect('/'); // Redireciona para a lista de disciplinas após a exclusão
    } catch (error) {
        res.status(500).send('Erro ao excluir a disciplina.'); // Retorna erro em caso de falha
    }
});