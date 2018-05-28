import pymysql

class UserDal(object):
    """ user database interface """

    mysql_config = {
        #'host': '127.0.0.1',
        #'port': 3306,
        'db': 'julian',
        'user': 'julianmacagno',
        'passwd': 'rivadavia850'
    }

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