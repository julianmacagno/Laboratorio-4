import pymysql
from flask import Flask, jsonify

class UserDal(object):
    """ user database interface """

    mysql_config = {
        #'host': '127.0.0.1',
        #'port': 3306,
        'db': 'julian',
        'user': 'julianmacagno',
        'passwd': 'rivadavia850'
    }

    def getAuditEvents(self, user):
        try:
            print("intentando devolver la lista de audits en el DAL")
            conn = pymysql.connect(**self.mysql_config)
            cursor = conn.cursor()
            cursor.execute("select * from credentials where username = '" + user['username'] + "' and admin = 'S'")
            
            if cursor.rowcount is 0:
                qst = "select username, event_id, date_format(event_date, '%d %m %Y %h:%i:%s') as datetime from audit_events where username = '" + user['username'] + "'"    
            else:
                qst = "select username, event_id, date_format(event_date, '%d %m %Y %h:%i:%s') as datetime from audit_events"
            
            cursor.execute(qst)
            rv = cursor.fetchall()
            payload = []
            content = {}
            for result in rv:
                content = {'username' : result[0],
                           'event_id': result[1],
                           'datetime': result[2] }
                payload.append(content)    
            conn.commit()
            conn.close()
            return payload
        except pymysql.err as err:
            print err
            print "MYSQL Exception"
            cursor.close()
            return False
            

    def insert(self, user):
        try:
            print("intento insertar en credentials")
            conn = pymysql.connect(**self.mysql_config)
            cursor = conn.cursor()
            qst = 'INSERT INTO credentials (username, password) VALUES (%s, %s)' #no comprueba que haya otro username pues el campo username tiene una constraint unique
            dst = (user['username'], user['password'])
            cursor.execute(qst, dst)
            conn.commit()
            conn.close()
            return True
        except: 
            cursor.close()
            return False

    
    def get(self, username):
        conn = pymysql.connect(**self.mysql_config)
        cursor = conn.cursor()
        qst = 'SELECT * FROM credentials WHERE username = %s'
        dst = (username)
        cursor.execute(qst, dst)
        conn.commit()
        conn.close()
        return cursor.fetchone() # ret puede contener tipo "none" el cual no es valido. habria que atrapar la excepcion antes de devolverla

    def log_on_audit_events(self, username, event):
        print("intentando " + event + " en audit_events")
        conn = pymysql.connect(**self.mysql_config)
        cursor = conn.cursor()
        paramList = [username, event]
        qst = "INSERT INTO audit_events (username, event_id) VALUES (%s, %s)"
        cursor.execute(qst, paramList)
        conn.commit()
        conn.close()
        return True 