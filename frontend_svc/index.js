'use strict';

const express = require('express');
const exphbs = require('express-handlebars');
const bodyParser = require('body-parser');
const handlers = require('./handlers');
const session = require('express-session');
const app = express();
const hbsOpts = {
    defaultLayout: 'main',
    extname: 'handlebars',
    layoutsDir: `${__dirname}/views/layouts/`,
    partialsDir: `${__dirname}/views/partials/`
}
const hbs = exphbs.create(hbsOpts);
app.engine('handlebars', hbs.engine);
app.set('view engine', 'handlebars');
app.use(session({
    secret: 'mys3cr3t',
    resave: false,
    saveUninitialized: true,
    cookie: { secure: false}}));
app.use(bodyParser.urlencoded({ extended: true }));

// route mapping
app.get('/', handlers.getBase);
app.get('/home', handlers.getHome);

app.get('/login', handlers.getLogin);
app.post('/login', handlers.postLogin);

app.get('/register', handlers.getRegister);
app.post('/register', handlers.postRegister);

app.get('/event', handlers.getEvents);
app.post('/event', handlers.postEvents);

app.get('/list', handlers.getList);
app.post('/list', handlers.postList);

app.post('/join', handlers.postJoin);

app.get('/newList', handlers.newList);
app.get('/newEvent', handlers.newEvent);
app.get('/newLocation', handlers.newLocation);

// startup sequence
const server = app.listen(8080, '127.0.0.1', () => {
    const host = server.address().address;
    const port = server.address().port;
    console.log('server is now listening on http://%s:%s', host, port);
})