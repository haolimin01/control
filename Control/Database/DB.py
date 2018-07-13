# status
import sqlite3
import json


class DB:
    DATABASE = '/Database/brain.sql'

    def __init__(self, table='status'):
        self.table = table
        self.conn = sqlite3.connect(DB.DATABASE)
        self.creat_table()

    def creat_table(self):
        creat_sql = 'CREATE TABLE IF NOT EXISTS "{0}" ("mac" TEXT PRIMARY KEY NOT NULL,' \
                    '"name" TEXT NOT NULL, "task" TEXT NOT NULL, "status" TEXT NOT NULL DEFAULT "working", ' \
                    '"limitation" INTEGER  DEFAULT 0, "maxup" INTEGER DEFAULT 0, "maxdown" INTEGER DEFAULT 0);'.format(self.table)
        self.conn.execute(creat_sql)

    def delete_table(self):
        delete_sql = 'DROP TABLE IF EXISTS "{0}";'.format(self.table)
        self.conn.execute(delete_sql)

    def insert(self, mac, name, task, status='working', limitation=0, maxup=0, maxdown=0):
        if not self.table_exist():
            self.creat_table()
        if self.mac_exist(mac=mac):
            #print('{0} is exist ...'.format(mac))
            return False
        else:
            if mac:
                insert_sql = "INSERT INTO '{0}' VALUES('{1}', '{2}', '{3}', '{4}', {5}, {6}, {7})"\
                             .format(self.table, mac, name, task, status, limitation, maxup, maxdown)
                self.conn.execute(insert_sql)
                self.conn.commit()
                return True
            else:
                #print('mac address in not exist ...')
                return False


    def delete(self, mac=''):
        if self.table_exist():
            if self.mac_exist(mac=mac):
                sql_str = "DELETE FROM {0} WHERE mac='{1}'".format(self.table, mac)
                self.conn.execute(sql_str)
                self.conn.commit()
                return True
            else:
                #print('mac address in not exist ...')
                return False
        else:
            #print('{0} in not exist ...'.format(self.table))
            return False

    def update_task(self, task, status, mac=''):
        if self.table_exist():
            if self.mac_exist(mac=mac):
                sql_str = "UPDATE {0} SET task='{1}', status='{2}' WHERE mac='{3}'".format(self.table, task, status, mac)
                self.conn.execute(sql_str)
                self.conn.commit()
                return True
            else:
                #print('mac address in not exist ...')
                return False
        else:
            #print('{0} in not exist ...'.format(self.table))
            return False

    def update_network(self, limitation, maxup, maxdown, mac=''):
        if self.table_exist():
            if self.mac_exist(mac=mac):
                print(limitation, maxup, maxdown, mac)
                sql_str = "UPDATE {0} SET limitation={1}, maxup={2}, maxdown={3} WHERE mac='{4}'".\
                          format(self.table, limitation, maxup, maxdown, mac)
                self.conn.execute(sql_str)
                self.conn.commit()
                return True
            else:
                #print('mac address in not exist ...')
                return False
        else:
            #print('{0} in not exist ...'.format(self.table))
            return False

    def query(self, mac=''):
        if self.table_exist():
            if self.mac_exist(mac=mac):
                sql_str = "SELECT * FROM {0} WHERE mac='{1}'".format(self.table, mac)
                cursor = self.conn.execute(sql_str)
                content = cursor.fetchone()
                data = {
                    'mac': content[0],
                    'name': content[1],
                    'task': content[2],
                    'status': content[3],
                    'limitation': content[4],
                    'maxup': content[5],
                    'maxdown': content[6]
                }
                return json.dumps(data)
            else:
                #print('mac address in not exist ...')
                return None
        else:
            #print('{0} in not exist ...'.format(self.table))
            return None

    def close(self):
        self.conn.close()

    def get_db_name(self):
        return self.table

    def display_all(self):
        if self.table_exist():
            display_sql = 'SELECT * FROM "{0}"'.format(self.table)
            cursor = self.conn.execute(display_sql)
            data = []
            index = 0
            for row in cursor:
                row_dict = {}
                row_dict['mac'] = row[0]
                row_dict['name'] = row[1]
                row_dict['task'] = row[2]
                row_dict['status'] = row[3]
                row_dict['limitation'] = row[4]
                row_dict['maxup'] = row[5]
                row_dict['maxdown'] = row[6]
                data.insert(index, row_dict)
                index += index
            return json.dumps(data, ensure_ascii=False)
        else:
            return None

    def table_exist(self):
        sql_str = "SELECT * FROM sqlite_master WHERE type='{0}' AND NAME='{1}'".format('table', self.table)
        cursor = self.conn.execute(sql_str)
        if cursor.fetchone():
            return True
        else:
            return False

    def mac_exist(self, mac):
        if not self.table_exist():
            return False
        elif not mac:
            return False
        else:
            sql_str = "SELECT * FROM {0} WHERE mac='{1}'".format(self.table, mac)
            cursor = self.conn.execute(sql_str)
            if cursor.fetchone():
                return True
            else:
                return False

