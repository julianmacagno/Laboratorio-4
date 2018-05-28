import json
from bottle import Bottle, route, run, get, template, post, request, response
from handlers.user import UserHandler

app = Bottle()
user_handler = UserHandler()

@app.post('/login')
def login():
    response.content_type = 'application/json'
    logged = user_handler.login(request)
    if logged:
        response.status = 200
        return json.dumps({'status': 'OK', 'logged': logged})
    else:
        response.status = 500
        return json.dumps({'status': 'ERROR', 'logged': logged})

@app.post('/register')
def register():
    response.content_type = 'application/json'
    created = user_handler.register(request)
    if created:
        response.status = 201
        print "se inserto correctamente en la base de datos"
        return json.dumps({'status': 'OK', 'created': created})
    else:
        response.status = 500
        print "no se pudo insertar en la bd"
        return json.dumps({'status': 'Error', 'created': created})

@app.post('/logout')
def logout():
    response.content_type = 'application/json'
    logged = user_handler.logout(request)
    
    if logged:
        print("Exito")
        response.status = 200
        return json.dumps({'status': 'OK'})
    
    else:
        print("Fracaso")
        response.status = 500
        return json.dumps({'status': 'Error'})

run(app, host='127.0.0.1', port=8081)