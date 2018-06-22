'use strict';

const express = require('express');
const exphbs = require('express-handlebars');
const session = require('express-session');
const bodyParser = require('body-parser');
const helpers = require('./helpers');
const jwt = require('jsonwebtoken');
const fs = require('fs');

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
app.use(session({
  secret: 'mys3cr3t',
  resave: false,
  saveUninitialized: true,
  cookie: { secure: false}
}));

app.get('/', (req, res) => {
  var sess = req.session;
  if(!sess.token) {
    console.log("No hay token");
    res.redirect("/login");
  } else {
    res.redirect("/home");
  }
});

app.get('/login', (req, res) => {
  var sess = req.session;
  if(!sess.token) {
    let loginParams = {};
    if(sess.loginError === "true") {
      loginParams = {
        errorMsg: sess.errorMsg
      }
    }
    res.render('login', loginParams);
  }
  else {
    res.redirect('/home');
  }    
});

app.post('/login', (req, res) => {
  const credentials = {
    username: req.body.username,
    password: req.body.password
  };

  var sess = req.session;
  helpers.login(credentials).then(body => {
    if(body.logged) {
      sess.token = body.token;
      res.redirect("/home"); //tengo que mandar el parametro del nombre de usuario que se setea en home.handlebars
    } else {
      console.log("Invalid credentials");
      sess.errorMsg = "Invalid credentials";
      sess.loginError = "true";
      res.redirect("/login");
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

  console.log("username:" + username.username);
  
  helpers.logout(username).then(resp => {
    if(resp) {
      req.session.token = null;
      req.session.loginError = "false";
      res.redirect('login');
      return;
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
  var sess = req.session
  if(!sess.token) {
    console.log("No hay token");
    res.redirect('/login');
    return;
  } else {

    let homeParams = {
      msg: 'hello',
      username: decryptToken(sess.token)
    };
  
    res.render('home', homeParams);
  }  
});

const decryptToken = function(token) {
  var opt = {
    algorithms: ["RS256"]
  }
  var decoded = jwt.verify(token, fs.readFileSync("../spt-auth-master/app/keypair.pub"), opt);
  return decoded.username
}

const server = app.listen(8080,'127.0.0.1', () => {
  const host = server.address().address;
  const port = server.address().port;
  console.log("server is now listening on http://%s:%s", host, port);
});
