import db
dbfile = "db/ferry.db"
db = db.DataModel(dbfile)


def migrate_tables():
    db.executeSQL(
        ''' 
            CREATE TABLE PORT (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                area VARCHAR(64) DEFAULT NULL,
                name VARCHAR(64) NOT NULL
            );

            CREATE TABLE VEHICLE_TYPE (
                type VARCHAR(64) PRIMARY KEY,
                fee FLOAT DEFAULT NULL,
                description VARCHAR(255) DEFAULT NULL
            );

            CREATE TABLE TICKET_TYPE (
                type VARCHAR(64) PRIMARY KEY,
                discount DECIMAL(3,2) DEFAULT NULL,
                description VARCHAR(255) DEFAULT NULL
            );

            CREATE TABLE COMPANY (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(32),
                api_url VARCHAR(64) DEFAULT NULL,
                api_psw VARCHAR(32) DEFAULT NULL
            );

            CREATE TABLE COUPON (
                code VARCHAR(8) PRIMARY KEY,
                discount DECIMAL(3,2) DEFAULT NULL
            ); 

            CREATE TABLE PAYMENT (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                insurance BINARY,
                sms BINARY,
                payment_date TEXT,
                total_cost FLOAT,
                payment_method VARCHAR(16),
                coupon_code VARCHAR(8) DEFAULT NULL,
                FOREIGN KEY (coupon_code) REFERENCES COUPON(code) ON DELETE SET DEFAULT ON UPDATE SET DEFAULT
            );

            CREATE TABLE PASSENGER (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fname VARCHAR(32),
                lname VARCHAR(32),
                country_code VARCHAR(3),
                phone_number VARCHAR(32),
                email VARCHAR(64),
                birthdate TEXT,
                id_card VARCHAR(16) UNIQUE
            );

            CREATE TABLE TRIP (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ship_name VARCHAR(64),
                ship_type VARCHAR(64),
                car_cap INTEGER,
                deck_cap INTEGER,
                air_cap INTEGER,
                dcab_cap INTEGER,
                qcab_cap INTEGER,
                company_id INTEGER DEFAULT NULL,
                
                FOREIGN KEY (company_id) REFERENCES COMPANY(id) ON DELETE CASCADE ON UPDATE CASCADE
            );

            CREATE TABLE ROUTE(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cost FLOAT,
                deck_cap INTEGER,
                dep_date TEXT,
                arr_date TEXT,
                route_seq INTEGER,
                dep_port_id INTEGER,
                arr_port_id INTEGER,
                trip_id INTEGER,
                
                
                FOREIGN KEY (trip_id) REFERENCES TRIP(id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (dep_port_id) REFERENCES PORT(id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (arr_port_id) REFERENCES PORT(id) ON DELETE CASCADE ON UPDATE CASCADE
            );

            CREATE TABLE TICKET (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_code VARCHAR(64) UNIQUE,
                cost FLOAT,
                special_seat VARCHAR(64),
                v_type VARCHAR(64),
                t_type VARCHAR(64),
                payment_id INTEGER,
                passenger_id INTEGER,
                trip_id INTEGER,
                
                FOREIGN KEY (v_type) REFERENCES VEHICLE_TYPE(type) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (t_type) REFERENCES TICKET_TYPE(type) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (payment_id) REFERENCES PAYMENT(id) ON DELETE SET NULL ON UPDATE CASCADE,
                FOREIGN KEY (passenger_id) REFERENCES PASSENGER(id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (trip_id) REFERENCES TRIP(id) ON DELETE CASCADE ON UPDATE CASCADE
            );
        ''')


def get_tables():
    try:
        tables = db.readData("SELECT name FROM sqlite_master WHERE type='table';")
        tables_to_drop = []
        for table in tables:
            tables_to_drop.append(table[0])
        return tables_to_drop
    except:
        return []


def drop_tables():
    tables = get_tables()
    for table in tables:
        if (table != 'sqlite_sequence'):
            db.executeSQL(
            f'''
                DROP TABLE IF EXISTS {table}
            ''',False)
    


def migrate():
    drop_tables()
    migrate_tables()


def main():
    print('Eloquent:')


if __name__ == '__main__':
    main()