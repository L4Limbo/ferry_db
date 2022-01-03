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

    def executeSQL(self, query, show=False):
        try:
            t1 = time.perf_counter()
            for statement in query.split(";"):
                if statement.strip():
                    self.cursor.execute(statement)
                    sql_time = time.perf_counter() - t1
                    print(f'εκτέλεση εντολής {statement[:40]}... σε {sql_time:.5f} sec')
            if show:
                for row in self.cursor.fetchall():
                    print(", ".join([str(item)for item in row]))
            self.con.commit()
            return True
        except sqlite3.Error as error:
            print(f"Σφάλμα εκτέλεσης εντολής SQL", error)
            return False
    
    def readTable(self, table):
        '''Φόρτωμα ενός πίνακα, όταν το προαιρετικό όρισμα machine πάρει τιμή, τότε επιστρέφει μόνο 
        τις εγγραφές που αφορούν τη συγκεκριμένη μηχανή'''
        try:
            query = f'''SELECT * FROM {table};'''
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            return records
            # result = []
            # for row in records:
            #     result.append(dict(row))
            # return result
        except sqlite3.Error as error:
            print(f"Σφάλμα φόρτωσης πίνακα {table}", error)


if __name__ == "__main__":
    dbfile = "db/ferry.db"
    ferry_db = DataModel(dbfile) # δημιουργία σύνδεσης στη βάση δεδομένων
