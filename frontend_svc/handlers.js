'use strict';

const API_BASE = 'virtserver.swaggerhub.com/LAB4_Final/LAB4_Final/1'
var request = require('request');
var fs = require("fs");
var jwt = require("jsonwebtoken");

const baseGetHandler = (req, res) => {
    const sess = req.session
    if(!sess.token) {
        res.redirect('login');
    }
    else {
        res.redirect('home');
    }
}

const loginGetHandler = (req, res) => {
    const session = req.session;
    if(session.token) {
        res.redirect('home');
        return;
    }
    res.render('login');
}

const loginPostHandler = (req, res) => {
    const session = req.session;
    const credentials = {
        email: req.body.email,
        password: req.body.password
    };
    const options = {
        headers: {'content-type' : 'application/json'},
        url: 'http://localhost:8082/users/login',
        body: JSON.stringify(credentials)
    };
    request.post(options, function (error, response, body){
        let data = JSON.parse(body);
        if(!error && response.statusCode == 200){
            if(data.Status == "OK"){
                session.token = data.Token
                res.redirect('/home')
            }
            else{
                res.redirect('/login')
            }
        }
        else{
            res.redirect('/login')
        }
    });
}

const registerGetHandler = (req, res) => {
    res.render('register');
}

const registerPostHandler = (req, res) => {
    const credentials = {
        username: req.body.username,
        email: req.body.email,
        password: req.body.password
    };
    const options = {
        headers: {'content-type' : 'application/json'},
        url: 'http://localhost:8082/users/register',
        body: JSON.stringify(credentials)
    };
    request.post(options, function (error, response, body){
        let data = JSON.parse(body);
        console.log(data)
        if(!error && response.statusCode == 200){
            if(data.Status == "OK"){
                res.redirect('/login')
            }
            else{
                res.redirect('/register')
            }
        }
        else{
            res.redirect('/register')
        }
    })
}

const eventsGetHandler = (req, res) => {
    var sess = req.session
    if(!sess.token) {
        res.redirect('/login');
        return;
    }

    const cert = fs.readFileSync("keypair.pub");
    const alg = {algorithms:["RS256"]}
    try{
        const payload = jwt.verify(sess.token,cert,alg)

        let eventName = req.param('name');
        let eventId = req.param('id');
        request.get("http://localhost:8081/events/filter?name=" + eventName, (req, resp) => {
        let event = JSON.parse(resp.body);

            request.get("http://localhost:8081/lists/filter?id_event=" + event[0].id, (req, resp) => {
                let lists = JSON.parse(resp.body);

                const params = {
                    eventName: event[0].name,
                    eventDate: event[0].date,
                    list: lists,
                    username: payload.username,
                    email: payload.email,
                    id: payload.id,
                    eventId: eventId
                }
                res.render('event', params);    
            });
        });
    }catch(err){
        console.log(err)
        sess.token = null;
        res.redirect('login')
    }
}

const homeGetHandler = (req, res) => {
    var sess = req.session
    if(!sess.token) {
        res.redirect('/login');
        return;
    }
    try { 
        const payload = jwt.verify(sess.token,fs.readFileSync("keypair.pub"),{algorithms:["RS256"]})
        
        request.get("http://localhost:8081/events", (req, resp) => {
            let events = JSON.parse(resp.body);
            const params = {
                eventos: events,
                username: payload.username,
                email: payload.email,
                id: payload.id
            }
            res.render('home', params);
        });
        
    } catch(err){
        console.log(err)
        sess.token = null;
        res.redirect('login')
    }
}

const listGetHandler = (req, res) => {
    var sess = req.session
    if(!sess.token) {
        res.redirect('/login');
        return;
    }    
    let listName = req.param('name');
    
    request.get("http://localhost:8081/lists/filter?name=" + listName, (req, resp) => {
        let list = JSON.parse(resp.body);
        
        request.get("http://localhost:8081/getListOwner?id=" + list[0].id, (req, resp) => {
            let owner = JSON.parse(resp.body);
            request.get("http://localhost:8081/getUserList?id=" + list[0].id, (req, resp) => {
                let userList = JSON.parse(resp.body);

                const params = {
                    listName: list[0].name,
                    listOwner: owner,
                    listId: list[0].id,
                    userList
                }
                console.log(params);
                res.render('list',params);    
            });
        });
    });
}

const joinPostHandler = (req, res) => {
    let listId = req.param('listId');
    let role = req.param('role');
    let listName = req.param('listName')
    var sess = req.session
    if(!sess.token) {
        res.redirect('/login');
        return;
    }
    try{
        const payload = jwt.verify(sess.token,fs.readFileSync("keypair.pub"),{algorithms:["RS256"]})
        let uri = "joinList?listId=" + listId + "&role=";
        uri += role + "&userId=" + payload.id;
        request.post("http://localhost:8081/" + uri,(req, resp) => {
            let re = JSON.parse(resp.body);
            if (re == false) {
                res.redirect('/home');
            }
            else {
                res.redirect('/list?name=' + listName);
            }
        });
        
    }catch(err){
        console.log(err)
        sess.token = null;
        res.redirect('login')
    }
}

const createNewList = (req, res) => {
    var sess = req.session
    if(!sess.token) {
        res.redirect('/login');
        return;
    }
    let eventName = req.param('eventName');
    let eventId = req.param('eventId');
    const params = {
        eventName: eventName,
        eventId: eventId
    }
    res.render('create-list', params);
}

const listPostHandler = (req, res) => {
    let sess = req.session;
    let eventName = req.body.eventName;
    let eventId = req.body.eventId;
    let listName = req.body.name;
    
    const list = {
        name: listName,
        event: eventName
    }
    console.log("eventid");
    console.log(eventId)
    console.log("json list");
    console.log(list);
    const options = {
        headers: {'content-type' : 'application/json'},
        url: 'http://localhost:8081/lists',
        body: JSON.stringify(list)
    };

    request.post(options, function (error, response, body) { 
        let data = JSON.parse(body);

        request.get("http://localhost:8081/lists/filter?name=" + listName, (req, resp) => {
            let actualList = JSON.parse(resp.body);
            
            console.log("Actual list");
            console.log(actualList[0].id);
            try{
                const payload = jwt.verify(sess.token, fs.readFileSync("keypair.pub"),{algorithms:["RS256"]});
                let uri = "joinList?listId=" + actualList[0].id + "&role=2&userId=" + payload.id;
                console.log(uri)
                request.post("http://localhost:8081/" + uri,(req, resp) => {
                    let re = JSON.parse(resp.body);
                    if (re == false) {
                        res.redirect('/event?name=' + eventName);
                    }
                    else {
                        res.redirect('/list?name=' + listName);
                    }
                });                
            }catch(err){
                console.log(err)
                sess.token = null;
                res.redirect('login')
            }
        });
    });   
}

const createNewEvent = (req, res) => {
    var sess = req.session
    if(!sess.token) {
        res.redirect('/login');
        return;
    }
    request.get("http://localhost:8081/locations", (req, resp) => {
       let locations = JSON.parse(resp.body);
       console.log(locations);
       const params = {
           locations: locations
       }
       res.render('create-event', params);
    });
}

const eventsPostHandler = (req, res) => {
    let id_location = req.body.location;
    let name = req.body.name;
    let date = req.body.date;
    const event = {
        id_location: id_location,
        name: name,
        date: date
    }

    const options = {
        headers: {'content-type' : 'application/json'},
        url: 'http://localhost:8081/events',
        body: JSON.stringify(event)
    };
    request.post(options, function (error, response, body){ 
        let data = JSON.parse(body);
        res.redirect('/home');
    });   
}

const newLocation = (req, res) => {
    var sess = req.session
    if(!sess.token) {
        res.redirect('/login');
        return;
    }
    res.render('create-location');
}

const locationPostHandler = (req,res) => {

}

module.exports = {
    getBase: baseGetHandler,
    getLogin: loginGetHandler,
    postLogin: loginPostHandler,
    getRegister: registerGetHandler,
    postRegister: registerPostHandler,
    getEvents: eventsGetHandler,
    postEvents: eventsPostHandler,
    getHome: homeGetHandler,
    getList: listGetHandler,
    postList: listPostHandler,
    postJoin: joinPostHandler,
    newList: createNewList,
    newEvent: createNewEvent,
    newLocation: newLocation
}