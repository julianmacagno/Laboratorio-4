from dal.dal import Dal

class LocationHelper(object):
    
    def __init__(self):
        self.dal = Dal()

    def createLocation(self, item):
        item = self.resolveItem(item)
        resp = self.dal.insertItem(item, 'location')
        return resp

    def getLocation(self, filters):
        if filters is not None:
            filters = self.resolveItem(filters)
        locations = self.dal.getItems(filters, 'location')
        return locations

    def updateLocation(self, item):
        item = self.resolveItem(item)   
        resp = self.dal.updateItem(item, 'location')
        return resp

    def getLocationName(self, item):
        print item['id']
        resp = self.dal.getLocationName_byLocationId(item['id'])
        return resp

    def resolveItem(self, item):
        if 'address' in item.keys():
            #if not 'coord' in item.keys():
                #ask Google for converting address to coord
                #add coord (key, value) to dict; and do below
            item.pop('address', None)

        if 'type' in item.keys():
            id_loc_type = self.dal.getIdType_ByTypeName(item['type'])
            item['id_loc_type'] = str(id_loc_type)
            item.pop('type', None)
        
        if 'owner' in item.keys():
            id_owner = self.dal.getUserId_ByUserName(item['owner'])
            item['id_owner'] = str(id_owner)
            item.pop('owner', None)
        return item