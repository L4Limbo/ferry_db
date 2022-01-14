import db
import pandas as pd
import random
import db
import migrate
import faker 
import functions as dbf

fake = faker.Faker()
dbfile = "db/ferry.db"
db = db.DataModel(dbfile)


def PortSeeder():
    ClearDB('PORT')
    ports = pd.read_csv('data_generation/el_ports.csv')
    for index, port in ports.iterrows():
        col = 'name'
        db.executeSQL(
            f'''
                INSERT INTO 'PORT' ('name') VALUES ('{port[col]}')
            ''')
    pass

def VehicleTypeSeeder():
    ClearDB('VEHICLE_TYPE')
    vehicle_types = pd.read_csv('data_generation/vehicle_types.csv')
    for index, vehicle_type in vehicle_types.iterrows():
        db.executeSQL(
            f'''
                INSERT INTO 'VEHICLE_TYPE' ('type','description','fee') 
                VALUES 
                ('{vehicle_type.type}','{vehicle_type.description}','{vehicle_type.fee}')
            ''')
    pass

def TicketTypeSeeder():
    ClearDB('TICKET_TYPE')
    ticket_types = pd.read_csv('data_generation/ticket_types.csv')
    for index, ticket_type in ticket_types.iterrows():
        if (str(ticket_type.description).lower()) == "nan":
            description = "null"
        else:
            description = ticket_type.description
        db.executeSQL(
            f'''
                INSERT INTO 'TICKET_TYPE' ('type','description','discount') 
                VALUES 
                ('{ticket_type.type}','{description}','{ticket_type.discount}')
            ''')
    pass

def SpecialSeatTypeSeeder():
    ClearDB('SPECIAL_SEAT_TYPE')
    special_seat_types = pd.read_csv('data_generation/special_types.csv')
    for index, special_seat_type in special_seat_types.iterrows():
        if (str(special_seat_type.description).lower()) == "nan":
            description = "null"
        else:
            description = special_seat_type.description
        db.executeSQL(
            f'''
                INSERT INTO 'SPECIAL_SEAT_TYPE' ('type','description','fee') 
                VALUES 
                ('{special_seat_type.type}','{description}','{special_seat_type.fee}')
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

def CouponSeeder():
    ClearDB('COUPON')
    coupons = pd.read_csv('data_generation/fake_coupons.csv')
    for index, coupon in coupons.iterrows():
        db.executeSQL(
            f'''
                INSERT INTO 'COUPON' ('code','discount')
                VALUES ('{coupon.code}','{coupon.discount}')
            ''')
    pass

def PaymentSeeder():
    ClearDB('PAYMENT')
    payments = pd.read_csv('data_generation/fake_payments.csv')
    for index, payment in payments.iterrows():
        db.executeSQL(
            f'''
                INSERT INTO 'PAYMENT' ('insurance','sms','payment_date','total_cost','payment_method','coupon_code')
                VALUES (0,0,'{payment.payment_date}',80.70,'{payment.payment_method}',null)
            ''')
    pass
    
def TripSeeder():
    ClearDB('TRIP')
    companies = db.readTable('COMPANY')
    companies_id = [company['id'] for company in companies]
    ships = pd.read_csv('data_generation/fake_ships.csv')
    for index, ship in ships.iterrows():
        company_id = random.choice(companies_id)
        description = fake.sentence()
        ship_name = ship['name']
        db.executeSQL(
            f'''
                INSERT INTO 'TRIP' ('ship_name','ship_type','company_id','deck_cap',
                'air_cap', 'dcab_cap', 'qcab_cap')
                VALUES ('{ship_name}','{ship.type}','{company_id}',150,50,20,40)
            ''')
    pass

def RouteSeeder():
    ClearDB('ROUTE')
    trips = db.readTable('TRIP')
    trip_ids = [trip['id'] for trip in trips]
    ports = db.readTable('PORT')
    port_ids = [port['id'] for port in ports]
    for i in range(0, len(trip_ids)):
        no_routes = random.randint(3, 6)
        cost = random.randint(5,10)
        arrival_date = fake.date_time_this_year()
        for j in range(0, no_routes):
            route_seq = j + 1
            if (j == 0):
                dep_port_id = random.choice(port_ids) 
            else:
                dep_port_id = arr_port_id
            arr_port_id = random.choice(port_ids) 
            departure_date = fake.date_time_between(start_date=arrival_date, end_date="+10h" )
            cost += random.randint(5,12);
            db.executeSQL(
                f''' 
                    INSERT INTO 'ROUTE' ('trip_id', 'dep_port_id','arr_port_id','arr_date','dep_date','cost','deck_cap','v_cap','route_seq')
                    VALUES ('{trip_ids[i]}','{dep_port_id}','{arr_port_id}','{arrival_date}','{departure_date}','{cost}',150,30,'{route_seq}')
                ''')
            arrival_date = departure_date   
    pass

def TicketSeeder():
    ClearDB('TICKET')
    tickets = pd.read_csv('data_generation/fake_tickets.csv')
    passengers = db.readTable('PASSENGER')
    passenger_ids = [passenger['id'] for passenger in passengers]
    trips = db.readTable('TRIP')
    trip_ids = [trip['id'] for trip in trips]
    payments = db.readTable('PAYMENT')
    payment_ids = [payment['id'] for payment in payments]
    
    vehicle_typess = db.readTable('VEHICLE_TYPE')
    vehicle_types = [vehicle_type['type'] for vehicle_type in vehicle_typess]
    
    ticket_typess = db.readTable('TICKET_TYPE')
    ticket_types = [ticket_type['type'] for ticket_type in ticket_typess]
    special_seats = ['Deck', 'Assigned Seat', '2 Bed Cabin (Single Bed)', '2 Bed Cabin (Whole Cabin)','4 Bed Cabin (Single Bed)','4 Bed Cabin (Whole Cabin)']
    for index, ticket in tickets.iterrows():
        passenger_id = random.choice(passenger_ids)
        trip_id = random.choice(trip_ids)
        payment_id = random.choice(payment_ids)
        v_type = random.choice(vehicle_types)
        t_type = random.choice(ticket_types)
        special_seat = random.choice(special_seats)
        db.executeSQL(
            f'''
                INSERT INTO 'TICKET' ('ticket_code','cost','special_seat','t_type','v_type','payment_id','passenger_id','trip_id')
                VALUES ('{ticket.ticket_code}',100,'{special_seat}','{t_type}','{v_type}','{payment_id}','{passenger_id}','{trip_id}')
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
    PortSeeder()
    VehicleTypeSeeder()
    TicketTypeSeeder()
    CompanySeeder()
    CouponSeeder()
    # PaymentSeeder()
    # PassengerSeeder()
    TripSeeder()
    RouteSeeder()
    PTPSeeder()
    pass


def PTPSeeder():
    ClearDB('PASSENGER')
    ClearDB('PAYMENT')
    ClearDB('TICKET')
    passengers = pd.read_csv('data_generation/fake_passengers.csv')
    trip_ids = db.readData(''' 
            SELECT id
            FROM TRIP                
            ''')
    trips = []
    for c in trip_ids:
        trips.append(c[0])
    
    tickets = []
    for index, passenger in passengers.iterrows():
        passenger_id = dbf.storePassenger(passenger.fname, passenger.lname, passenger.country_code,
                           passenger.phone_number, passenger.email, passenger.birthdate, passenger.id_card)
        trip_id = random.choice(trips)
        ticket_cost = dbf.getTripCost(trip_id, random.randint(1, 2), random.randint(2,3))
        tickets.append([passenger_id, ticket_cost, trip_id])
        
    print(tickets)
    for i in range(0,len(tickets),2):
        payment_cost = tickets[i][1] + tickets[i+1][1]
        payment_id = dbf.storePayment(payment_cost, 0, 0, '2022-01-14', 'paypal', None)
        # payment_id = int(db.cursor.lastrowid)
        print(payment_id)
        dbf.storeTicket(fake.ean(8), tickets[i][1], None, None, 'Adult', payment_id, int(tickets[i][0]), int(tickets[i][2]))
        dbf.storeTicket(fake.ean(8), tickets[i+1][1], None, None, 'Adult', payment_id, int(tickets[i+1][0]), int(tickets[i+1][2]))

def main():
    print('Eloquent:')


if __name__ == '__main__':
    main()