import faker
import random
import pandas as pd 
import string

fake = faker.Faker('en_GB');


def ports_generation():
    pass
    # https://ec.europa.eu/eurostat/cache/metadata/Annexes/mar_esms_an2.xlsx
    # df = pd.read_csv('data_generation/ports.csv',encoding='cp1252')
    # df2 = df[['CTRY', 'Country/Port Name']]
    # df2 = df2[df2.CTRY == 'EL']
    # df2.to_csv('data_generation/el_ports.csv')
    
def vehicle_type_generation():
    df = pd.DataFrame(columns=['type','description','fee'])
    data = [
       {
            'type': 'Car',
            'description': '(Vehicles up to 5m long and 2m high)',
            'fee': 1.5
       },
       {
            'type': 'Motorcycle',
            'description': '(All motorcycles)',
            'fee': 0.5
       },
       {
            'type': 'Truck',
            'description': 'Vehicles up to 8m long and 3.5m high',
            'fee': 2.0
       }
    ]
    df = df.append(data, ignore_index=True)
    df.to_csv('data_generation/vehicle_types.csv')
    
def ticket_type_generation():
    df = pd.DataFrame(columns=['type','description','discount'])
    data = [
       {
            'type': 'Adult',
            'description': 'null',
            'discount': 0.0
       },
       {
            'type': 'Infant',
            'description': '(Ages: 0 - 5)',
            'discount': 1.0
       },
       {
            'type': 'Child',
            'description': '(Ages: 5 - 16)',
            'discount': 0.25
       },
       {
            'type': 'Student',
            'description': 'null',
            'discount': 0.5
       },
       {
            'type': 'Senior',
            'description': 'null',
            'discount': 0.5
       },
       {
            'type': 'Passenger with reduced mobility',
            'description': 'null',
            'discount': 0.25
       },
       {
            'type': 'Greek military personel',
            'description': 'null',
            'discount': 1.0
       },
    ]
    df = df.append(data, ignore_index=True)
    df.to_csv('data_generation/ticket_types.csv')
    
def special_seat_type_generation():
    df = pd.DataFrame(columns=['type','description','fee'])
    data = [
       {
            'type': 'Assigned Seat',
            'description': 'null',
            'fee': 0.2
       },
       {
            'type': '2 Bed Cabin (Single Bed)',
            'description': 'null',
            'fee': 1.0
       },
       {
            'type': '2 Bed Cabin (Whole Cabin)',
            'description': 'null',
            'fee': 2.0
       },
       {
            'type': '4 Bed Cabin (Single Bed)',
            'description': 'null',
            'fee': 1.0
       },
       {
            'type': '4 Bed Cabin (Whole Cabin)',
            'description': 'null',
            'fee': 4.0
       }
    ]
    df = df.append(data, ignore_index=True)
    df.to_csv('data_generation/special_types.csv')

def fake_companies(count=3):
    df = pd.DataFrame(columns=['name','api_url','api_psw'])
    for i in range(0, count):
        data = {'name': fake.company(),
                'api_url': fake.domain_name(),
                'api_psw': fake.swift(8)}

        df = df.append(data, ignore_index=True)
    df.to_csv('data_generation/fake_companies.csv')

def fake_coupons(count=10):
    df = pd.DataFrame(columns=['code','discount'])
    for i in range(0, count):
        data = {'code': fake.word().upper(),
                'discount': random.choice([0.1, 0.15, 0.25])}
        df = df.append(data, ignore_index=True) 
    df.to_csv('data_generation/fake_coupons.csv')
    
def fake_payments(count=20):
    df = pd.DataFrame(columns=['insurance','sms', 'payment_date', 'payment_method'])
    payment_methods = ['master-card', 'paypal', 'bitcoin', 'visa', 'paysafe']
    for i in range(0, count):
        data = {'insurance': random.randint(0, 1),
                'sms': random.randint(0, 1),       
                'payment_date': fake.date_time(), 
                'payment_method': random.choice(payment_methods)
                }
        df = df.append(data, ignore_index=True)
    df.to_csv('data_generation/fake_payments.csv')

def fake_passengers(count=10):
    df = pd.DataFrame(columns=['fname','lname','country_code','phone_number','email','birthdate','id_card'])
    for i in range(0, count):
        data = {'fname': fake.name().split()[0],
                'lname': fake.name().split()[1],
                'country_code': fake.country_code(),
                'phone_number': fake.phone_number(),
                'email': fake.email(),
                'birthdate': fake.date_of_birth(),
                'id_card': 2*random.choice(string.ascii_letters).upper() + fake.ean(8)}
        df = df.append(data, ignore_index=True) 
    df.to_csv('data_generation/fake_passengers.csv')

def fake_tickets(count=10):
    df = pd.DataFrame(columns=['ticket_code','t_type','v_type'])
    categories = ['Adult', 'Infant', 'Child', 'Student','Greek military personel','Passenger with reduced mobility','Senior']
    vehicles = ['Car','Bicyle','Truck','Van']
    for i in range(0, count):
        data = {'ticket_code': fake.ean(8),
                'special_seat': 'null',
                't_type': random.choice(categories),
                'v_type': 'null'}
        data['v_type'] = random.choice(vehicles) if(data['t_type']!='Child' or data['t_type']!='Infant') else 'null'
        df = df.append(data, ignore_index=True)
    df.to_csv('data_generation/fake_tickets.csv')

def fake_ships(count=20):
    df = pd.DataFrame(columns=['name', 'type'])
    ship_types = ['high-speed', 'passenger', 'roll-on-roll-off', ]
    for i in range(0, count):
        data = {'name': fake.name().split()[0],
                'type': random.choice(ship_types)}
        df = df.append(data, ignore_index=True)
    df.to_csv('data_generation/fake_ships.csv')
    
def fake_generation(count=10):
    # ports_generation()
    vehicle_type_generation()
    ticket_type_generation()
    fake_companies(3)
    fake_coupons(10)
    fake_payments(20)
    fake_passengers(20)
    fake_tickets(10)
    fake_ships(20)
    
def main():
    print('Generator')
    
    
if __name__ == '__main__':
    main()