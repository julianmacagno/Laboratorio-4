import json, os, datetime
import python_jwt as jwt
# import Crypto.PublicKey.RSA as RSA
from bottle import Bottle, route, run, get, template, post, request, response
from helpers.locations_helper import LocationHelper
from helpers.event_helper import EventHelper
from helpers.list_helper import ListHelper

locationHelper = LocationHelper()
eventHelper = EventHelper()
listHelper = ListHelper()
app = Bottle()
response.default_content_type = 'application/json'

@app.get('/test')
def test():
    return json.dumps({'test': 'OK'})

@app.post('/locations')
def createLocation():
    resp = locationHelper.createLocation(request.json)
    return json.dumps(resp)

@app.put('/locations')
def updateLocation():
    resp = locationHelper.updateLocation(request.json)
    return json.dumps(resp)

@app.get('/locations')
def getLocation():
    resp = locationHelper.getLocation(None)
    return json.dumps(resp)

@app.get('/locations/filter')
def getLocationByFilters():
    filters = dict(request.query)
    resp = locationHelper.getLocation(filters)
    return json.dumps(resp)

@app.post('/events')
def createEvent():
    resp = eventHelper.createEvent(request.json)
    return json.dumps(resp)

@app.put('/events')
def updateEvent():
    resp = eventHelper.updateEvent(request.json)
    return json.dumps(resp)

@app.get('/events')
def getEvent():
    resp = eventHelper.getEvent(None)
    print resp
    return json.dumps(resp)

@app.get('/events/filter')
def getEventByFilters():
    filters = dict(request.query)
    resp = eventHelper.getEvent(filters)
    return json.dumps(resp)

@app.post('/lists')
def createList():
    resp = listHelper.createList(request.json)
    return json.dumps(resp)

@app.put('/lists')
def updateList():
    resp = listHelper.updateList(request.json)
    return json.dumps(resp)

@app.get('/lists')
def getList():
    resp = listHelper.getList(None)
    return json.dumps(resp)

@app.get('/lists/filter')
def getListByFilters():
    filters = dict(request.query)
    resp = listHelper.getList(filters)
    return json.dumps(resp)

@app.get('/locNameById')
def getLocNameById():
    filters = dict(request.query)
    resp = locationHelper.getLocationName(filters)
    return json.dumps(resp)

@app.get('/getListOwner')
def getListOwner():
    filters = dict(request.query)
    resp = listHelper.getListOwner(filters)
    return json.dumps(resp)

@app.get('/getUserList')
def getUserList():
    filter = dict(request.query)
    resp = listHelper.getUserList(filter)
    return json.dumps(resp)

@app.post('/joinList')
def joinList():
    filter = dict(request.query)
    resp = listHelper.joinList(filter)
    return json.dumps(resp)

@app.get('/getEventId')
def getEventId():
    filter = dict(request.query)
    resp = eventHelper.getEventId(filter)
    return json.dumps(resp)

run(app, host='127.0.0.1', port=8081)