import json, os, datetime
import python_jwt as jwt
import Crypto.PublicKey.RSA as RSA
from bottle import Bottle, route, run, get, template, post, request, response
from handlers.user import UserHandler

app = Bottle()
user_handler = UserHandler()

@app.post('/audit')
def audit():
    response.content_type = 'application/json'
    audit = user_handler.audit(request)
    return json.dumps({'status': 'OK', 'audit': audit})

@app.post('/login')
def login():
    response.content_type = 'application/json'
    logged = user_handler.login(request)
    if logged:
        data = request.json
        payload = {'username': str(data['username'])}
    	token = generate_token(payload)
        response.status = 200
        return json.dumps({'status': 'OK', 'logged': logged, 'token': token})
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

def generate_token(payload):
    private_key_file = os.path.join(os.path.dirname(__file__), 'keypair.priv')
    with open(private_key_file, 'r') as fd:
        private_key = RSA.importKey(fd.read())
    token = jwt.generate_jwt(payload,private_key,'RS256',datetime.timedelta(minutes=5))
    return token

def validate_token(token):
    payload = {'userid': '1234', 'role': 'admin'}
    public_key_file = os.path.join(os.path.dirname(__file__), 'keypair.pub')
    with open(public_key_file, 'r') as fd:
        public_key = RSA.importKey(fd.read())
    try:
        header, claims = jwt.verify_jwt(token,public_key,['RS256'])
    except jwt.exceptions.SignatureError:
        print ('invalid token signature')
        raise SystemExit()
    for k in payload: assert claims[k] == payload[k]

run(app, host='127.0.0.1', port=8081)