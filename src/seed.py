import db
import pandas as pd
import random
import db
import migrate
import faker 


fake = faker.Faker()
dbfile = "db/ferry.db"
db = db.DataModel(dbfile)


def HarborSeeder():
    ClearDB('HARBOR')
    ports = pd.read_csv('data_generation/el_ports.csv')
    for index, port in ports.iterrows():
        col = 'name'
        db.executeSQL(
            f'''
                INSERT INTO 'HARBOR' ('name') VALUES ('{port[col]}')
            ''')
    pass


def PassengerSeeder():
    ClearDB('PASSENGER')
    passengers = pd.read_csv('data_generation/fake_passengers.csv')
    for index, passenger in passengers.iterrows():
        db.executeSQL(
            f'''
                INSERT INTO 'PASSENGER' ('fname','lname','country_code',
                'phone_number','email','nationality','birthdate')
                VALUES ('{passenger.fname}','{passenger.lname}','{passenger.country_code}',
                '{passenger.phone_number}','{passenger.email}','{passenger.nationality}','{passenger.birthdate}')
            ''')
    pass


def TicketSeeder():
    ClearDB('TICKET')
    tickets = pd.read_csv('data_generation/fake_tickets.csv')
    passengers = db.readTable('PASSENGER')
    passengers_id = [passenger['id'] for passenger in passengers]
    routes = db.readTable('ROUTE')
    routes_id = [route['id'] for route in routes]
    for index, ticket in tickets.iterrows():
        passenger_id = random.choice(passengers_id)
        route_id = random.choice(routes_id)
        db.executeSQL(
            f'''
                INSERT INTO 'TICKET' ('ticket_code','category','vehicle','passenger_id','route_id')
                VALUES ('{ticket.ticket_code}','{ticket.category}','{ticket.vehicle}','{passenger_id}','{route_id}')
            ''')
    pass


def CouponSeeder():
    ClearDB('COUPON')
    coupons = pd.read_csv('data_generation/fake_coupons.csv')
    for index, coupon in coupons.iterrows():
        db.executeSQL(
            f'''
                INSERT INTO 'COUPON' ('code','used')
                VALUES ('{coupon.code}','{coupon.used}')
            ''')
    pass


def SpecialSeatSeeder():
    ClearDB('SPECIAL_SEAT')
    pass


def RouteSeeder(count=10):
    ClearDB('ROUTE')
    companies = db.readTable('COMPANY')
    companies_id = [company['id'] for company in companies]
    for i in range(0, count):
        company_id = random.choice(companies_id)
        description = fake.sentence()
        db.executeSQL(
            f'''
                INSERT INTO 'ROUTE' ('description','company_id')
                VALUES ('{description}','{company_id}')
            ''')
    pass


def ShipSeeder():
    ClearDB('SHIP')
    ships = pd.read_csv('data_generation/fake_ships.csv')
    services = db.readTable('SERVICE')
    services_id = [service['id'] for service in services]
    companies = db.readTable('COMPANY')
    companies_id = [company['id'] for company in companies]
    for index, ship in ships.iterrows():
        service_id = random.choice(services_id)
        company_id = random.choice(companies_id)
        db.executeSQL(
            f'''
                INSERT INTO 'SHIP' ('name','type','availability','fullness','service_id','company_id')
                VALUES ('{ship.name}','{ship.type}','{ship.availability}','{ship.fullness}',
                '{service_id}','{company_id}')
            ''')
    pass


def CompanySeeder():
    ClearDB('COMPANY')
    companies = pd.read_csv('data_generation/fake_companies.csv')
    for index, company in companies.iterrows():
        db.executeSQL(
            f'''
                INSERT INTO 'COMPANY' ('name','api_url','api_psw')
                VALUES ('{company.name}','{company.api_url}','{company.api_psw}')
            ''')
    pass


def ServiceSeeder():
    ClearDB('SERVICE')
    services = pd.read_csv('data_generation/fake_services.csv')
    for index, service in services.iterrows():
        db.executeSQL(
            f'''
                INSERT INTO 'SERVICE' ('name')
                VALUES ('{service.name}')
            ''')
    pass 


def StationSeeder():
    ClearDB('STATION')
    routes = db.readTable('ROUTE')
    routes_id = [route['id'] for route in routes]
    harbors = db.readTable('HARBOR')
    harbors_id = [harbor['id'] for harbor in harbors]
    for i in range(0, len(routes_id)):
        no_stations = random.randint(3, 6)
        cost = -5
        arrival_date = fake.date_time_this_year()
        for j in range(0, no_stations):
            harbor_id = random.choice(harbors_id)
            arrival_date = fake.date_time_between(start_date=arrival_date, end_date="+10h" )
            cost += 5
            db.executeSQL(
                f''' 
                    INSERT INTO 'STATION' ('route_id', 'harbor_id','arrival_date','cost')
                    VALUES ('{routes_id[i]}','{harbor_id}','{arrival_date}','{cost}')
                ''')         
    pass

    
def ClearDB(table="null"):
    if table != "null":
        db.executeSQL(
            f'''
                DELETE FROM {table}
            ''')
        return
    for table in migrate.get_tables():
        if (table != 'sqlite_sequence'):
            db.executeSQL(
            f'''
                DELETE FROM {table}
            ''')
    pass

  
def Seed(fresh=True):
    if(fresh):
        ClearDB()
    HarborSeeder()
    CompanySeeder()
    PassengerSeeder()
    CouponSeeder()
    ServiceSeeder()
    ShipSeeder()
    RouteSeeder()
    StationSeeder()
    TicketSeeder()
    pass


def main():
    print('Eloquent:')


if __name__ == '__main__':
    main()