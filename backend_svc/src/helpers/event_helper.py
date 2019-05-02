from dal.dal import Dal

class EventHelper(object):
    
    def __init__(self):
        self.dal = Dal()

    def createEvent(self, item):
        item = self.resolveItem(item)
        resp = self.dal.insertItem(item, 'event')
        return resp

    def getEvent(self, filters):
        if filters is not None:
            filters = self.resolveItem(filters)
        locations = self.dal.getItems(filters, 'event')
        locations = self.resolveDatetime(locations)
        return locations

    def updateEvent(self, item):
        item = self.resolveItem(item)   
        resp = self.dal.updateItem(item, 'event')
        return resp

    def resolveItem(self, item):
        if 'location' in item.keys():
            id_location = self.dal.getLocationId_ByLocationName(item['location'])
            item['id_location'] = str(id_location)
            item.pop('location', None)
        return item
    
    def resolveDatetime(self, item):
        for i in range(len(item)):
            if 'date' in item[i]:
                item[i]['date'] = item[i]['date'].__str__()
        return item

    def getEventId(self, filter):
        resp = self.dal.getEventId_byEventName(filter['name'])
        return resp