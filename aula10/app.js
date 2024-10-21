// Bibliotecas
const express = require('express');
const { Sequelize, DataTypes } = require('sequelize');
const bodyParser = require('body-parser');
const exphbs = require('express-handlebars');
const path = require('path');

// Configurações
const app = express();
const PORTA = 3000;

// Configuração do Handlebars como motor de templates
app.engine('handlebars', exphbs());
app.set('view engine', 'handlebars');
app.set('views', path.join(__dirname, 'views'));

// Middleware
app.use(bodyParser.urlencoded({ extended: false }));

// Configuração do banco de dados
const sequelize = new Sequelize({
    dialect: 'sqlite',
    storage: 'academico.db'
});

// Modelo do banco de dados
const Disciplina = sequelize.define('Disciplina', {
    nome: {
        type: DataTypes.STRING,
        allowNull: false
    },
    carga_horaria: {
        type: DataTypes.INTEGER,
        allowNull: false
    },
    professor: {
        type: DataTypes.STRING,
        allowNull: false
    }
});

// Rota para a página inicial
app.get('/', async (req, res) => {
    const disciplinas = await Disciplina.findAll();
    res.render('index', { disciplinas });
});

// Rota para adicionar uma nova disciplina
app.get('/add', (req, res) => {
    res.render('add');
});

app.post('/add', async (req, res) => {
    const { nome, carga_horaria, professor } = req.body;
    await Disciplina.create({ nome, carga_horaria: parseInt(carga_horaria), professor });
    res.redirect('/');
});

// Rota para editar uma disciplina
app.get('/edit/:id', async (req, res) => {
    const disciplina = await Disciplina.findByPk(req.params.id);
    if (!disciplina) {
        return res.status(404).send('Disciplina não encontrada');
    }
    res.render('edit', { disciplina });
});

app.post('/edit/:id', async (req, res) => {
    const disciplina = await Disciplina.findByPk(req.params.id);
    if (!disciplina) {
        return res.status(404).send('Disciplina não encontrada');
    }
    const { nome, carga_horaria, professor } = req.body;
    disciplina.nome = nome;
    disciplina.carga_horaria = parseInt(carga_horaria);
    disciplina.professor = professor;
    await disciplina.save();
    res.redirect('/');
});

// Rota para excluir uma disciplina
app.get('/delete/:id', async (req, res) => {
    const disciplina = await Disciplina.findByPk(req.params.id);
    if (!disciplina) {
        return res.status(404).send('Disciplina não encontrada');
    }
    res.render('delete', { disciplina });
});

app.post('/delete/:id', async (req, res) => {
    const disciplina = await Disciplina.findByPk(req.params.id);
    if (!disciplina) {
        return res.status(404).send('Disciplina não encontrada');
    }
    await disciplina.destroy();
    res.redirect('/');
});

// Inicializar a aplicação
sequelize.sync().then(() => {
    app.listen(PORTA, () => {
        console.log(`Servidor rodando em http://localhost:${PORTA}`);
    });
}).catch(error => {
    console.error('Não foi possível conectar ao banco de dados:', error);
});