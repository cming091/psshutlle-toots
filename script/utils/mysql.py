#encoding=utf-8
import sys
import traceback
from functools import wraps
import pymysql

def singleton(cls):
    instances = dict()
    @wraps(cls)
    def get_instance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return get_instance


@singleton
class Mysql:

    def __init__(self, host, port, user, passwd):
        self.host = host
        self.port = int(port)
        self.user = user
        self.passwd = passwd
        self.conn = {}
        self.cursor = {}
        self.connect_db = {}

    def get_connection(self, db_name):
        try:
            self.disconnect(db_name, close_all=False)
            self.conn[db_name] = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.passwd,
                                                 db=db_name,charset='utf8')
            self.cursor[db_name] = self.conn[db_name].cursor()
            self.connect_db[db_name] = True
            return True
        except:
            print('---mysql connect error')
            traceback.print_exc()
            return False

    def execute(self, db, sql):
        # print('[db:{} sql:{},cusor:{}]'.format(db,sql,self.cursor.get(db)))
        results = None
        try:
            results=self.cursor.get(db).execute(sql)
            self.conn.get(db).commit()
            rs = self.cursor.get(db).fetchall()
            if rs:
                results=rs
        except Exception as e:
            print('---mysql exec error',e)
            traceback.print_exc()
            self.conn.get(db).rollback()
        finally:
            return results

    def disconnect(self, db_name='', close_all=False):
        if not close_all:
            if self.cursor.get(db_name):
                self.cursor[db_name].close()
            if self.conn.get(db_name):
                self.conn[db_name].close()
            if self.connect_db.get(db_name):
                self.connect_db[db_name] = False
        else:
            if self.cursor:
                for i_db, i_cursor in self.cursor.items():
                    i_cursor.close()
            if self.conn:
                for i_db, i_conn in self.conn.items():
                    i_conn.close()
            if self.connect_db:
                self.connect_db.clear()
