import faker
import random
import pandas as pd 

fake = faker.Faker('en_GB');


def fake_passengers(count=10):
    df = pd.DataFrame(columns=['fname','lname','country_code','phone_number','email','nationality','birthdate'])
    for i in range(0, count):
        data = {'fname': fake.name().split()[0],
                'lname': fake.name().split()[1],
                'country_code': fake.country_code(),
                'phone_number': fake.phone_number(),
                'email': fake.email(),
                'nationality': fake.country(),
                'birthdate': fake.date_of_birth()}
        df = df.append(data, ignore_index=True) 
    df.to_csv('data_generation/fake_passengers.csv')
    

def fake_coupons(count=10):
    df = pd.DataFrame(columns=['code','used'])
    for i in range(0, count):
        data = {'code': fake.word().upper(),
                'used': random.randint(0, 1)}
        df = df.append(data, ignore_index=True) 
    df.to_csv('data_generation/fake_coupons.csv')


def fake_tickets(count=10):
    df = pd.DataFrame(columns=['ticket_code','category','vehicle'])
    categories = ['Adult', 'Infant', 'Child', 'Student']
    vehicles = ['Car','Bicyle','Truck','Van']
    for i in range(0, count):
        data = {'ticket_code': fake.ean(8),
                'category': random.choice(categories),
                'vehicle': 'null'}
        data['vehicle'] = random.choice(vehicles) if(data['category']=='Adult') else 'null'
        df = df.append(data, ignore_index=True)
    df.to_csv('data_generation/fake_tickets.csv')


def fake_companies(count=3):
    df = pd.DataFrame(columns=['name','api_url','api_psw'])
    for i in range(0, count):
        data = {'name': fake.company(),
                'api_url': fake.domain_name(),
                'api_psw': fake.swift(8)}

        df = df.append(data, ignore_index=True)
    df.to_csv('data_generation/fake_companies.csv')


def fake_ships(count=20):
    df = pd.DataFrame(columns=['name','availability','fullness','type'])
    ship_types = ['high-speed', 'passenger', 'roll-on-roll-off', ]
    for i in range(0, count):
        data = {'name': fake.name().split()[0],
                'availability': random.randint(300, 1000),
                'fullness': random.randint(100, 300),
                'type': random.choice(ship_types)}
        df = df.append(data, ignore_index=True)
    df.to_csv('data_generation/fake_ships.csv')
    
    
def ports_generation(count=10):
    pass
    # https://ec.europa.eu/eurostat/cache/metadata/Annexes/mar_esms_an2.xlsx
    # df = pd.read_csv('data_generation/ports.csv',encoding='cp1252')
    # df2 = df[['CTRY', 'Country/Port Name']]
    # df2 = df2[df2.CTRY == 'EL']
    # df2.to_csv('data_generation/el_ports.csv')


def fake_services(count=0):
    df = pd.DataFrame(columns=['name'])
    services = ['restaurant', 'cabins', 'vehicles', 'wifi', 'etickets']
    for i in range(0, len(services)):
        data = {'name': services[i]}
        
        df = df.append(data, ignore_index=True)
    df.to_csv('data_generation/fake_services.csv')
    
    
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
    

def fake_special_seats(count=40):
    df = pd.DataFrame(columns=['insurance','sms', 'payment_date', 'payment_method'])
    types = ['deck', 'cabin', 'vip', 'airplane']
    for i in range(0, count):
        data = {'type': random.choice(types),
                'availability': random.randint(0, 100),       
                'description': fake.sentence(), 
                'no_seat': "No" + str(random.randint(1, 50)),
                'no_bed': random.randint(1, 6)
                }
        df = df.append(data, ignore_index=True)
    df.to_csv('data_generation/fake_special_seats.csv')
    

def fake_generation(count=10):
    fake_coupons(count)
    fake_passengers(count)
    fake_tickets(count)
    fake_companies()
    fake_ships()
    fake_services()
    fake_payments()
    fake_special_seats()
    

def main():
    print('Generator')
    
    
if __name__ == '__main__':
    main()