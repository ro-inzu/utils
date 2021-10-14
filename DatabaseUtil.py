import os

import pyodbc as db
import pymysql as sql
from configs import EnvironmentConfig
import inspect

env_obj = EnvironmentConfig()


class Database(object):
    def __init__(self, conn_type, server, db_name, driver_port, user=None, pw=None):
        self.con = None
        db.pooling = False
        if conn_type == 'sqlserver':
            try:
                if user is None and pw is None:
                    self.con = db.connect(
                        f'DRIVER={driver_port};Server={server};Database={db_name};Trusted_connection=yes')
                else:
                    self.con = db.connect(
                        f'DRIVER={driver_port};Server={server};Database={db_name};UID={user};PWD={pw}')
            except Exception as e:
                print(e)
        elif conn_type == 'mysql':
            try:
                self.con = sql.connect(host=server, user=user, passwd=pw, db=db_name, port=int(driver_port))
            except Exception as e:
                print(e)
        if self.con is None:
            print('No connection to {} {}'.format(server, db_name))
        else:
            self.cursor = self.con.cursor()

    @classmethod
    def connect_server(cls):
        print('fnc: {}'.format(inspect.getframeinfo(inspect.currentframe()).function))
        conn_type = env_obj.get_connection()
        server = env_obj.get_server()
        db_name = env_obj.get_db()
        driver = env_obj.get_odbc_driver()
        return cls(conn_type, server, db_name, driver)

    @classmethod
    def connect_server_two(cls):
        print('fnc: {}'.format(inspect.getframeinfo(inspect.currentframe()).function))
        conn_type = env_obj.get_connection()
        host = env_obj.get_host()
        db_name = env_obj.get_db()
        user = env_obj.get_user()
        pw = env_obj.get_pw()
        driver = env_obj.get_port()
        return cls(conn_type, host, db_name, driver, user, pw)

        return cls(conn_type, server, db_name, driver, user, pw)

    def fetch(self, query):
        print('fnc: {}'.format(inspect.getframeinfo(inspect.currentframe()).function))
        data = ''
        try:
            self.cursor.execute(query)
            data = self.cursor.fetchall()
        except Exception as e:
            print(e)
        else:
            self.cursor.close()
            del self.cursor
            self.con.close()
        return data

    def update(self, query):
        print('fnc: {}'.format(inspect.getframeinfo(inspect.currentframe()).function))
        try:
            self.cursor.execute(query)
            self.con.commit()
        except Exception as e:
            print(e)
        else:
            self.cursor.close()
            del self.cursor
            self.con.close()
