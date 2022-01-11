import db

dbfile = "db/ferry.db"
db = db.DataModel(dbfile)


def migrate_tables():
    db.executeSQL(
        ''' 
            CREATE TABLE HARBOR (
                id integer PRIMARY KEY AUTOINCREMENT,
                area varchar(32) DEFAULT NULL,
                name varchar(32) NOT NULL
            );
            
            CREATE TABLE COMPANY (
                id integer PRIMARY KEY AUTOINCREMENT,
                name varchar(32),
                api_url varchar(64) DEFAULT NULL,
                api_psw varchar(32) DEFAULT NULL
            );
            
            CREATE TABLE PASSENGER (
                id integer PRIMARY KEY AUTOINCREMENT,
                fname varchar(32),
                lname varchar(32),
                country_code integer,
                phone_number varchar(32),
                email varchar(64),
                nationality varchar(64),
                birthdate datetime
            );
            
            CREATE TABLE COUPON (
                id integer PRIMARY KEY AUTOINCREMENT,
                code varchar(10),
                used binary
            );
            
            CREATE TABLE SERVICE (
                id integer PRIMARY KEY AUTOINCREMENT,
                name varchar(32)
            );
            
            CREATE TABLE SHIP (
                id integer PRIMARY KEY AUTOINCREMENT,
                name varchar(32) NOT NULL,
                type varchar(32) NOT NULL,
                availability integer DEFAULT NULL,
                fullness integer DEFAULT NULL,
                service_id integer,
                company_id integer,
                FOREIGN KEY (service_id) REFERENCES SERVICE(id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (company_id) REFERENCES COMPANY(id) ON DELETE CASCADE ON UPDATE CASCADE
            );
            
            CREATE TABLE SPECIAL_SEAT (
                id integer PRIMARY KEY AUTOINCREMENT,
                type varchar (32),
                availability binary,
                description varchar(128),
                no_seat varchar(8),
                no_bed integer DEFAULT NULL,
                ship_id binary DEFAULT NULL,
                FOREIGN KEY (ship_id) REFERENCES SHIP(id) ON DELETE CASCADE ON UPDATE CASCADE
            );
            
            CREATE TABLE ROUTE (
                id integer PRIMARY KEY AUTOINCREMENT,
                description varhar(128),
                company_id integer,
                ship_id integer,
                FOREIGN KEY (ship_id) REFERENCES SHIP(id) ON DELETE CASCADE ON UPDATE CASCADE
                FOREIGN KEY (company_id) REFERENCES COMPANY(id) ON DELETE CASCADE ON UPDATE CASCADE
            );

            CREATE TABLE STATION (
                route_id integer,
                harbor_id integer,
                arrival_date datetime,
                cost float,
                FOREIGN KEY (route_id) REFERENCES ROUTE(id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (harbor_id) REFERENCES HARBOR(id) ON DELETE CASCADE ON UPDATE CASCADE
            );   
            
            CREATE TABLE TICKET (
                id integer PRIMARY KEY AUTOINCREMENT,
                ticket_code varchar(32) NOT NULL,
                cost float,
                category varchar(32),
                vehicle varchar(16),
                payment_id integer,
                passenger_id integer,
                special_seat_id integer ,
                route_id integer,
                FOREIGN KEY (payment_id) REFERENCES PAYMENT(id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (passenger_id) REFERENCES PASSENGER(id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (special_seat_id) REFERENCES SPECIAL_SEAT(id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (special_seat_id) REFERENCES ROUTE(id) ON DELETE CASCADE ON UPDATE CASCADE
            );

            CREATE TABLE PAYMENT (
                id integer PRIMARY KEY AUTOINCREMENT,
                insurance binary,
                sms binary,
                payment_date datetime,
                total_Cost float,
                payment_method varchar(16),
                coupon_id integer,
                FOREIGN KEY (coupon_id) REFERENCES COUPON(id) ON DELETE CASCADE ON UPDATE CASCADE
            );
        ''')


def get_tables():
    tables = db.readTable('sqlite_master')
    tables_to_drop = []
    for row in tables:
        tables_to_drop.append(row['name'])
    return tables_to_drop


def drop_tables():
    for table in get_tables():
        if (table != 'sqlite_sequence'):
            db.executeSQL(
            f'''
                DROP TABLE IF EXISTS {table}
            ''')


def migrate():
    drop_tables()
    migrate_tables()


def main():
    print('Eloquent:')


if __name__ == '__main__':
    main()