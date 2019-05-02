import pymysql

class Dal(object):
    mysql_config = {
        #'host': '127.0.0.1',
        #'port': 3306,
        'db': 'julian',
        'user': 'julianmacagno',
        'passwd': 'rivadavia850'}

    def __init__(self):
        self.conn = pymysql.connect(**self.mysql_config)
        self.cursor = self.conn.cursor()
        self.dictCursor = self.conn.cursor(pymysql.cursors.DictCursor)

    def insertItem(self, item, tablename):
        try:
            keys = item.keys()
            for i in keys:
                if i == 'id':
                    keys.remove('id')
            query = "INSERT INTO " + tablename + " ("
            for i in range(len(keys)):
                query += keys[i] + ", "
            query = query[0:query.rfind(',')] + ") VALUES ("
            for i in range(len(keys)):
                try:
                    float(item[keys[i]])
                    query += item[keys[i]] + ", "
                except ValueError:
                    query += "'" + item[keys[i]] + "', "
            query = query[0:query.rfind(',')] + ");"
            print query
            self.cursor.execute(query)
            self.conn.commit()
            return True
        except pymysql.err as err:
            print err
            return False

    def updateItem(self, item, tablename):
        try:
            keys = item.keys()
            keys.remove('id')
            query = "UPDATE " + tablename + " SET "
            for i in keys:
                query+= i + " = "
                try:
                    float(item[i])
                    query += item[i] + ", "
                except ValueError:
                    query += "'" + item[i] + "', "
            query = query[:-2]
            query+= " WHERE id = " + item['id'] +");"
            self.cursor.execute(query)
            self.conn.commit()
            return True
        except pymsql.err as err:
            print err
            return False

    def getItems(self, filters, tablename):
        try:
            query = "SELECT * FROM " + tablename
            if filters is not None:
                keys = filters.keys()
                query+= " WHERE "
                for i in keys:
                    try:
                        float(filters[i])
                        query +=  i + " = " + filters[i] + " AND "
                    except ValueError:
                        query += i + " = '" + filters[i] + "' AND "
                query = query[:-5]
            print query
            self.dictCursor.execute(query)
            resp = self.dictCursor.fetchall()
            return resp
        except pymysql.err as err:
            print err
            return False

    def getIdType_ByTypeName(self, typeName):
        try:
            self.cursor.execute("SELECT id FROM location_type WHERE name = '" + typeName + "';")
            res = self.cursor.fetchone()
            return res[0]
        except pymysql.err as err:
            print err
            return False
    
    def getUserId_ByUserName(self, userName):
        try:
            self.cursor.execute("SELECT id FROM user WHERE name = '" + userName + "';")
            res = self.cursor.fetchone()
            return res[0]
        except pymysql.err as err:
            print err
            return False
    
    def getLocationId_ByLocationName(self, locationName):
        try:
            self.cursor.execute("SELECT id FROM location WHERE name = '" + locationName + "';")
            res = self.cursor.fetchone()
            return res[0]
        except pymysql.err as err:
            print err
            return False

    def getLocationName_byLocationId(self, locationId):
        try:
            self.cursor.execute("SELECT name FROM location WHERE id = '" + locationId + "';")
            res = self.cursor.fetchone()
            return res[0]
        except pymysql.err as err:
            print err
            return False

    def getEventId_ByEventName(self, eventName):
        try:
            self.cursor.execute("SELECT id FROM event WHERE name = '" + eventName + "';")
            res = self.cursor.fetchone()
            return res[0]
        except pymysql.err as err:
            print err
            return False
    
    def getListOwner(self, id):
        try:
            self.cursor.execute("select id_user from user_list where id_guest_list = " + id +" and id_role=2;")
            res = self.cursor.fetchone()
            self.cursor.execute("select name from user where id =" + str(res[0]) + ";")
            res2 = self.cursor.fetchone()
            return res2[0]
        except pymysql.err as err:
            print err
            return False

    def getUserList(self, id):
        try:
            self.dictCursor.execute("select u.name from user_list ul join user u on u.id = ul.id_user where id_guest_list = " + str(id) + ";")
            res = self.dictCursor.fetchall()
            return res
        except pymysql.err as err:
            print err
            return False

    def joinList(self, filter):
        try:
            query = "insert into user_list values (" + str(filter['listId']) + "," + str(filter['userId']) + "," + str(filter['role']) + ");"
            print query
            self.cursor.execute(query)
            res = self.cursor.fetchall()
            self.conn.commit()
            if res == ():
                return True
            else:
                return False
        except Exception as err:
            print err
            return False

