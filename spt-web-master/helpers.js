const request = require('request');
const AUTH_SERVICE_PATH = 'http://localhost:8081';

const logout = username => {
  let options = {
    url: `${AUTH_SERVICE_PATH}/logout`,
    headers: {
      'content-type': 'application/json'
    },
    body: JSON.stringify(username)
  };

  return new Promise((resolve, reject) => {
    request.post(options, (err, res, body) => {
      if(err) reject(err);
      else resolve(JSON.parse(body)['created']);
    });
  });
};

const login = credentials => {
  let options = {
    url: `${AUTH_SERVICE_PATH}/login`,
    headers: {
      'content-type': 'application/json'
    },
    body: JSON.stringify(credentials)
  };
  
  return new Promise((resolve, reject) => {
    request.post(options, (err, res, body) => {
      if(err) reject(err);
      else resolve(JSON.parse(body)['logged']);
    });
  });
};

const register = credentials => {
  let options = {
    url: `${AUTH_SERVICE_PATH}/register`,
    headers: {
      'content-type': 'application/json'
    },
    body: JSON.stringify(credentials)
  };

  return new Promise((resolve, reject) => {
    request.post(options, (err, res, body) => {
      if(err) reject(err);
      else resolve(JSON.parse(body)['created']);
    });
  });
};

module.exports = {
  login: login,
  register: register,
  logout: logout
}