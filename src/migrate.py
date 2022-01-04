import connect

dbfile = "db/ferry.db"
db = connect.DataModel(dbfile)


def migrate_tables():
    db.executeSQL(
        ''' 
            CREATE TABLE ROUTE (
                id integer PRIMARY KEY AUTOINCREMENT,
                departure_date datetime,
                arrival_date datetime,
                duration time,
                company_id integer
            );

            CREATE TABLE HARBOR (
                id integer PRIMARY KEY AUTOINCREMENT,
                area varchar,
                name varchar
            );

            CREATE TABLE COMPANY (
                id integer PRIMARY KEY AUTOINCREMENT,
                name varchar,
                api_url varchar,
                api_psw varchar
            );

            CREATE TABLE SHIP (
                id integer PRIMARY KEY AUTOINCREMENT,
                name varchar,
                type varchar,
                availability integer,
                fullness integer,
                service_id integer,
                company_id integer
            );

            CREATE TABLE SPECIAL_SEAT (
                id integer PRIMARY KEY AUTOINCREMENT,
                type varchar,
                availability binary,
                description text,
                no_seat varchar,
                no_bed integer,
                ship_id binary
            );

            CREATE TABLE TICKET (
                id integer PRIMARY KEY AUTOINCREMENT,
                name string,
                cost float,
                category string,
                vehicle string,
                payment_id integer,
                passenger_id integer,
                special_seat_id integer,
                route_id integer
            );

            CREATE TABLE PAYMENT (
                Id integer PRIMARY KEY AUTOINCREMENT,
                insurance binary,
                sms binary,
                payment_date datetime,
                total_Cost float,
                payment_method varchar,
                coupon_id integer
            );

            CREATE TABLE PASSENGER (
                id integer PRIMARY KEY AUTOINCREMENT,
                fname varchar,
                lname varchar,
                country_code integer,
                phone_number varchar,
                email varchar,
                nationality varchar,
                birthdate datetime
            );

            CREATE TABLE SERVICES (
                id integer PRIMARY KEY AUTOINCREMENT,
                name varchar
            );

            CREATE TABLE COUPON (
                id integer PRIMARY KEY AUTOINCREMENT,
                code varchar,
                used binary
            );

            CREATE TABLE STATION (
                route_id integer,
                harbor_id integer,
                arrival_date datetime
            );   
        ''')


def get_tables():
    tables = db.readTable('sqlite_master')
    
    tables_to_drop = []
    for row in tables:
        tables_to_drop.append(row[1])
    return tables_to_drop


def drop_tables():
    for table in get_tables():
        if (table != 'sqlite_sequence'):
            db.executeSQL(
            f'''
                DROP TABLE IF EXISTS {table}
            ''')


def main():
    print('Eloquent:')


if __name__ == '__main__':
    main()