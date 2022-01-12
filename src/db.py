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
            print("Επιτυχής σύνδεση στη βάση δεδομένων", filename)
            self.cursor.execute("select sqlite_version();")
            record = self.cursor.fetchall()
            for rec in record:
                print("SQLite Database Version is: ", rec[0])
        except sqlite3.Error as error:
            print("Σφάλμα σύνδεσης στη βάση δεδομένων sqlite", error)
    
    
    def close(self):
        self.con.commit()
        self.con.close()


    def executeSQL(self, query, fkeys=True):
        try:
            t1 = time.perf_counter()
            for statement in query.split(";"):
                if statement.strip():
                    if(fkeys):
                        self.cursor.execute('PRAGMA FOREIGN_KEYS = on')
                    else:
                        self.cursor.execute('PRAGMA FOREIGN_KEYS = off')
                    self.cursor.execute(statement)
                    sql_time = time.perf_counter() - t1
                    print(f'εκτέλεση εντολής {statement[:40]}... σε {sql_time:.5f} sec')
            self.con.commit()
            return True
        except sqlite3.Error as error:
            print(f"Σφάλμα εκτέλεσης εντολής SQL", error)
            return False
    
    
    def readTable(self, table):
        '''Φόρτωμα ενός πίνακα, όταν το προαιρετικό όρισμα machine πάρει τιμή, τότε επιστρέφει μόνο 
        τις εγγραφές που αφορούν τη συγκεκριμένη μηχανή'''
        try:
            self.cursor.execute('PRAGMA FOREIGN_KEYS = on')
            query = f'''SELECT * FROM {table};'''
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            return self.toJSON(table, records)
        except sqlite3.Error as error:
            print(f"Σφάλμα φόρτωσης πίνακα {table}", error)
            
            
    def readData(self, query):
        try:
            self.cursor.execute('PRAGMA FOREIGN_KEYS = on')
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            return records
        except sqlite3.Error as error:
            print(f"Σφάλμα φόρτωσης πίνακα", error)
    
    
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
            print(f"Σφάλμα φόρτωσης πίνακα {table}", error)
        

if __name__ == "__main__":
    dbfile = "db/ferry.db"
    ferry_db = DataModel(dbfile) # δημιουργία σύνδεσης στη βάση δεδομένων
