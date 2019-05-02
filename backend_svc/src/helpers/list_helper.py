from dal.dal import Dal

class ListHelper(object):
    
    def __init__(self):
        self.dal = Dal()

    def createList(self, item):
        item = self.resolveItem(item)
        resp = self.dal.insertItem(item, 'guest_list')
        return resp

    def getList(self, filters):
        if filters is not None:
            filters = self.resolveItem(filters)
        locations = self.dal.getItems(filters, 'guest_list')
        return locations

    def updateList(self, item):
        item = self.resolveItem(item)   
        resp = self.dal.updateItem(item, 'guest_list')
        return resp

    def getListOwner(self, filter):
        resp = self.dal.getListOwner(filter['id'])
        return resp

    def getUserList(self, filter):
        resp = self.dal.getUserList(filter['id'])
        return resp

    def joinList(self, filter):
        resp = self.dal.joinList(filter)
        return resp    

    def resolveItem(self, item):
        if 'event' in item.keys():
            id_event = self.dal.getEventId_ByEventName(item['event'])
            item['id_event'] = str(id_event)
            item.pop('event', None)
        return item