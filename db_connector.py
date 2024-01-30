import sqlite3

class Database:
    # Initalise database object
    def __init__(self):
        self.DBname = 'database.db'
    
    # Database connection method
    def connect(self):
        conn = None
        try:
            conn = sqlite3.connect(self.DBname)
        except Exception as e:
            print(e)
    
        return conn
    
    # Database disconnection method
    def disconnect(self, conn):
        conn.close()

    def queryDB(self, command, params=[]):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(command, params)
        result = cur.fetchall()
        self.disconnect(conn)
        return result
    
    # Update database method
    def updateDB(self, command, params=[]):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(command, params)
        conn.commit()
        result = cur.fetchall()
        self.disconnect(conn)
        return result
    
    # Get table columns
    def get_table_info(self, table_name):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(f'PRAGMA table_info({table_name})')
        result = cur.fetchall()
        field_names = [info[1] for info in result]
        self.disconnect()
        return result