# -*- coding: utf-8 -*-

import sqlite3
import time


class DataModel():
    def __init__(self, filename):
        self.filename = filename
        try:
            self.con = sqlite3.connect(filename)
            self.row_factory = sqlite3.Row
            self.cursor = self.con.cursor()
##            print("Succesful connection to Database", filename)
            self.cursor.execute("select sqlite_version();")
            record = self.cursor.fetchall()
            for rec in record:
                pass
##                print("SQLite Database Version is: ", rec[0])
        except sqlite3.Error as error:
            pass
##            print("Error when trying to connect to sqlite database", error)
    
    
    def close(self):
        self.con.commit()
        self.con.close()


    def executeSQL(self, query, params=(), fkeys=True):
        try:
            t1 = time.perf_counter()
            for statement in query.split(";"):
                if statement.strip():
                    if(fkeys):
                        self.cursor.execute('PRAGMA FOREIGN_KEYS = on')
                    else:
                        self.cursor.execute('PRAGMA FOREIGN_KEYS = off')
                    self.cursor.execute(statement,params)
                    sql_time = time.perf_counter() - t1
##                    print(f'execute command {statement[:30]}... in {sql_time:.4f} sec')
            self.con.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as error:
##            print(f"Error executing SQL command", error)
            return False
    
    
    def readTable(self, table):
        try:
            self.cursor.execute('PRAGMA FOREIGN_KEYS = on')
            query = f'''SELECT * FROM {table};'''
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            return self.toJSON(table, records)
        except sqlite3.Error as error:
            pass
##            print(f"Error loading table {table}", error)
            
            
    def readData(self, query):
        try:
            self.cursor.execute('PRAGMA FOREIGN_KEYS = on')
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            return records
        except sqlite3.Error as error:
            pass
##            print(f"Error loading table", error)
    
    
    def toJSON(self, table, results):
        try:
            query = f'''PRAGMA table_info({table});'''
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            cols = []
            for record in records:
                cols.append(record[1])
            pretty_res=[]
            for result in results:
                res = {cols[i]: list(result)[i] for i in range(len(cols))}
                pretty_res.append(res)          
            return pretty_res
        except sqlite3.Error as error:
            pass
##            print(f"Error loading table {table}", error)
        

if __name__ == "__main__":
    dbfile = "ferry.db"
    ferry_db = DataModel(dbfile)
