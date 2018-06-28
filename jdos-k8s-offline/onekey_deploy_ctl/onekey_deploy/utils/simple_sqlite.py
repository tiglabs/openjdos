# -*- coding:utf-8 -*-

##
import os
import sqlite3
from api_service.task_message import Task_Message


class CON_DB_ERR(Exception):
    def __init__(self):
        pass


class OPER_DB_ERR(Exception):
    def __init__(self):
        pass


class cluster_sqlplite3():
    def __init__(self, db_dir='/etc/onekey_deploy/', db_name='clusert.db'):

        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
        self.conn = None
        db_file = db_dir + db_name
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        create_tabel_if_not_exits = '''
          create table if not  exists environments (
            environment_id text primary key, 
            environment_type int, 
            environment_params text, 
            environment_progress real, 
            environment_status text,
            environment_result bool, 
            environment_desc text,
            environment_time text,
            environment_err int);'''
        # try:
        self.conn.execute(create_tabel_if_not_exits)
        # except:
        #    raise CON_DB_ERR

    def insert(self, Task_Message, id):

        if type(Task_Message) == dict:
            insert_sql = '''insert into environments values("%s",%d,"%s","%s","%s","%s","%s","%s","%d")''' \
                         % (id,
                            Task_Message.get("environment_type"),
                            Task_Message.get("environment_params"),
                            Task_Message.get("environment_progress"),
                            Task_Message.get("environment_status"),
                            Task_Message.get("environment_result"),
                            Task_Message.get("environment_desc"),
                            Task_Message.get("environment_time"),
                            Task_Message.get("environment_err"),
                            )
        else:
            insert_sql = '''insert into environments values("%s",%d,"%s","%s","%s","%s","%s","%s",%d)''' \
                         % (id,
                            Task_Message.environment_type,
                            Task_Message.environment_params,
                            Task_Message.environment_progress,
                            Task_Message.environment_status,
                            Task_Message.environment_result,
                            Task_Message.environment_desc,
                            Task_Message.environment_time,
                            Task_Message.environment_err,
                            )
        cursor = self.conn.cursor()
        # print insert_sql
        try:
            cursor.execute(insert_sql)
        except:
            raise OPER_DB_ERR
        cursor.close()
        self.conn.commit()

    def select(self, col_name=None, col_vaule=None):

        if (not col_name) or (not col_vaule):
            select_sql = '''select * from environments'''
        else:
            select_sql = '''select * from 'environments' whereis %s=%s''' % (col_name, col_vaule)

        cursor = self.conn.cursor()
        try:
            cursor.execute(select_sql)
        except:
            raise OPER_DB_ERR
        vaules = cursor.fetchall()
        cursor.close()
        return vaules

    def update(self, Task_Message, id):
        if type(Task_Message) == dict:
            update_sql = '''update environments set 
                            "environment_type" = %d,
                            "environment_params" = "%s",
                            "environment_progress" = "%s",
                            "environment_status" = "%s",
                            "environment_result" = "%s",
                            "environment_desc" = "%s",
                            "environment_time" = "%s",
                            "environment_err" = %d where environment_id = "%s"''' \
                         % (Task_Message.get("environment_type"),
                            Task_Message.get("environment_params"),
                            Task_Message.get("environment_progress"),
                            Task_Message.get("environment_status"),
                            Task_Message.get("environment_result"),
                            Task_Message.get("environment_desc"),
                            Task_Message.get("environment_time"),
                            Task_Message.get("environment_err"),
                            id
                            )
        else:
            update_sql = '''update environments set 
                            "environment_type" = %d,
                            "environment_params" = "%s",
                            "environment_progress" = "%s",
                            "environment_status" = "%s",
                            "environment_result" = "%s",
                            "environment_desc" = "%s",
                            "environment_time" = "%s",
                            "environment_err" = %d where environment_id = "%s"''' \
                         % (Task_Message.environment_type,
                            Task_Message.environment_params,
                            Task_Message.environment_progress,
                            Task_Message.environment_status,
                            Task_Message.environment_result,
                            Task_Message.environment_desc,
                            Task_Message.environment_time,
                            Task_Message.environment_err,
                            id
                            )
        cursor = self.conn.cursor()
        try:
            cursor.execute(update_sql)
        except:
            raise OPER_DB_ERR
        cursor.close()
        self.conn.commit()
# if __name__ == '__main__':
#    try:
#        sqltest = cluster_sqlplite3()
#    except CON_DB_ERR:
#        print "connetc sql error"
#    sqltest.insert()
