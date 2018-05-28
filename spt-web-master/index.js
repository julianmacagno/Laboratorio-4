'use strict';

const express = require('express');
const exphbs = require('express-handlebars');
const bodyParser = require('body-parser');
const helpers = require('./helpers');

const app = express();

const hbsOpts = {
  defaultLayout: 'main',
  extname: 'handlebars',
  layoutsDir: __dirname + '/views/layouts/'
}
const hbs = exphbs.create(hbsOpts);

app.engine('handlebars', hbs.engine);
app.set('view engine','handlebars');

app.use(bodyParser.urlencoded({extended: true}));

app.get('/', (req, res) => {
  res.redirect('login');
});

app.get('/login', (req, res) => {
  res.render('login');
});

app.post('/login', (req, res) => {
  const credentials = {
    username: req.body.username,
    password: req.body.password
  };

  helpers.login(credentials).then(logged => {
    if(logged) {
      let loginParams = {
        username: credentials.username
      };
      res.render('home', loginParams);
    } else {
      let loginParams = {
      errorMsg: "invalid credentials"
      };
      res.render('login', loginParams);
    }
  }, err => {
    console.error(err);
  });
});

app.get('/register', (req, res) => {
  res.render('register');
});

app.post('/register', (req, res) => {
  const credentials = {
    username: req.body.username,
    password: req.body.password
  }
  
  helpers.register(credentials).then(created => {
    if(created) {
      res.redirect('login');
    } else {
      let registerParams = {
        errorMsg: "user could not be created, try again"
      };
      res.render('register', registerParams);
    }
  }, err => {
    console.error(err);
  });
});

app.post('/logout', (req, res) => {
  const username = {
    username: req.body.username
  }

  console.log("username:" + username);
  
  helpers.logout(username).then(created => {
    if(created) {
      res.redirect('login');
    } else {
      let logoutParams = {
        errorMsg: "username could not be passed, try again"
      };
      res.render('login', logoutParams);
    }
  }, err => {
    console.error(err);
  });
});


app.get('/home', (req, res) => {
  let homeParams = {
    msg: 'hello'
  };

  res.render('home', homeParams);
});

const server = app.listen(8080,'127.0.0.1', () => {
  const host = server.address().address;
  const port = server.address().port;
  console.log("server is now listening on http://%s:%s", host, port);
});
