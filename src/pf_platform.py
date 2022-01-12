import random

def randate():
    
    dd = str(random.randint(1,31))

    if len(dd) == 1:

        dd = '0' + dd

    mm = str(random.randint(1,1))

    if len(mm) == 1:

        mm = '0' + mm

    yy = str(random.randint(21,21))

    h = str(random.randint(0,23))

    if len(h) == 1:

        h = '0' + h

    m = str(random.randint(0,59))

    if len(m) == 1:

        m = '0' + m

    date = [dd + '/' + mm + '/' + yy, h + ':' + m]

    return date



def generate_trips(N):

    port = ['Athens','Chania','Santorini','Kalamata','Chios','Thessaloniki','Nayplio','Mykonos','Mitilini']

    company = ['Minoan Lines', 'Blue Star Ferries', 'ANEK Lines', 'Sea Jets', 'Aegean Speed Lines']

    trips = []
    
    for i in range(0,N):

        dep = port[random.randint(0,len(port)-1)]

        arr = port[random.randint(0,len(port)-1)]

        c = company[random.randint(0,len(company)-1)]

        pas = random.randint(0,30)

        veh = random.randint(0,5)
        
        if dep != arr:

            trips.append([dep,arr,randate(),c,pas,veh])

    return trips,port,company


trips,port,company = generate_trips(10000)

lot = []

for el in trips:

    x = el[0:2]

    if x not in lot:

        lot.append(x)

lot.sort()


while True:
    
    ans = input('input: ')

    if ans == 'leave':

        break

    if ans == 'ports':

        print('----------------\n')

        for el in port:

            print(el)

        print('----------------\n')

    if ans == 'trips':

        print('----------------\n')

        for el in lot:

            print(el[0] + ' - ' + el[1])

        print('----------------\n')

    if ans == 'search':

        print('----------------\n')

        dep_port = input('Departure port: ')

        arr_port = input('Arrival port: ')

        ret = input('Return? (y/n): ')

        dep_date = input('Departure date (dd/mm/yy): ')

        if ret == 'y':
            
            ret_date = input('Return date (dd/mm/yy): ')

        pas = int(input('Number of passengers: '))

        veh = int(input('Number of vehicles: '))

        print('\nAvailable Departure Trips:')
        for el in trips:

            if el[0] == dep_port:

                if el[1] == arr_port:

                    if el[2][0] == dep_date:

                        if el[4] >= pas:

                            if el[5] >= veh:

                                print(el)

        if ret == 'y':
            
            print('\nAvailable Return Trips:')
            for el in trips:

                if el[0] == arr_port:

                    if el[1] == dep_port:

                        if el[2][0] == ret_date:

                            if el[4] >= pas:

                                if el[5] >= veh:

                                    print(el)

        print('----------------\n')

        

        

        



