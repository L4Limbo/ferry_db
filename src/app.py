import functions as dbf
from datetime import datetime


def myDictDisp(dic):

    print('\n\n')

    for key, value in dic.items():
        
        print(key, ' : ', value)


def searchTrips(dep_port, arr_port, dep_date):

    var = []

    temp = dbf.findPorts(dep_port,arr_port, dep_date)

    for el in temp:

        trip = {}

        trip_id = el[0]
        dep_rs = el[1]
        arr_rs = el[2]

        trip['id'] = trip_id
        trip['dep_rs'] = dep_rs
        trip['arr_rs'] = arr_rs

        trip['av_deck'] = dbf.getTotalCap(trip_id,dep_rs,arr_rs)[0][0]
        trip['av_veh'] = dbf.getTotalVehicleCap(trip_id,dep_rs,arr_rs)[0][0]

        booked_ss = dbf.getSpecialSeats(trip_id)
        total_ss = dbf.getTripCapacity(trip_id)

        trip['av_seat'] = total_ss[0][0] - booked_ss[4][0]
        trip['av_dualcabin'] = total_ss[0][1] - booked_ss[0][0] - booked_ss[1][0] * 2
        trip['av_quadcabin'] = total_ss[0][2] - booked_ss[2][0] - booked_ss[3][0] * 4

        trip['base_cost'] = dbf.getTripCost(trip_id, dep_rs, arr_rs)

        trip['stations'] = dbf.getTripStations(trip_id, dep_rs, arr_rs)

        trip['trip_info'] = dbf.getTripInfo(trip_id)[0]
        
        var.append(trip)

    trips = []

    for el in var:

        if el['av_deck'] >= numofpas and el['av_veh'] >= 4*numofveh:

            trips.append(el)

    return trips
    

##

def inTicketParams(trip):

    tickets = []
    
    print('''\nTicket types:
0. Adult
1. Infant
2. Child
3. Student
4. Senior
5. Passenger with reduced mobility
6. Greek military personel''')

    print('\nTicket classes: \n0. Deck (' + str(trip['av_deck']) + ' available)'
    '\n1. Assigned Seat (' + str(trip['av_seat']) + ' available)'
    '\n2. 2 Bed Cabin (Single Bed) (' + str(trip['av_dualcabin']) + ' available)'
    '\n3. 2 Bed Cabin (Whole Bed) (' + str(trip['av_dualcabin']//2) + ' available)'
    '\n4. 4 Bed Cabin (Single Bed) (' + str(trip['av_quadcabin']) + ' available)'
    '\n5. 4 Bed Cabin (Whole Bed) (' + str(trip['av_quadcabin']//4) + ' available)')

    print('\nVehicle types: \n0. Car (' + str(trip['av_veh']//2) + ' slots available)'
    '\n1. Motorcycle (' + str(trip['av_veh']) + ' slots available)'
    '\n2. Truck (' + str(trip['av_veh']//4) + ' slots available)\n\n')
        
    for i in range(0,numofpas):
        
        route = {}
        info = {}
        vehicle = {}
        ticket = {}
        
        info['ticket_type'] = input('Passenger ' + str(i+1) + ' ticket type: ')

        info['ticket_class'] = input('Passenger ' + str(i+1) + ' ticket class: ')

        ticket['info'] = info

        route['dep_port'] = dep_port

        route['arr_port'] = arr_port

        ticket['trip'] = trip

        vehicle['vehicle_type'] = None

        ticket['vehicle'] = vehicle

        tickets.append(ticket)

    for i in range(0,numofveh):

        while True:

            p = int(input('\nVehicle ' + str(i+1) + ' is assigned to passenger: '))
            
            if tickets[p-1]['vehicle']['vehicle_type'] == None and tickets[p-1]['info']['ticket_type']!='Infant' and tickets[p-1]['info']['ticket_type']!='Child':

                tickets[p-1]['vehicle']={'vehicle_type' : input('Vehicle ' + str(i+1) + ' type: ')}

                break

            else:

                print('''Passenger has already been assigned a vehicle or cannot be assigned one.
Please try again''')


    return tickets

##

while True:
    
    x = input('''<><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
Welcome to the ProjectFerry app!
Type \'book\' to search for tickets\n''')

    if x == 'book':

        dep_port = input('\nDeparture port: ')

        arr_port = input('Arrival port: ')

        ret = input('Round trip? (y/n): ')

        dep_date = input('Departure date (YYYY-MM-DD): ')

        if ret == 'y':

            ret_date = input('Return date (YYYY-MM-DD): ')

        numofpas = int(input('Number of passengers: '))

        numofveh = int(input('Number of vehicles: '))

        iterable = []

        trips = searchTrips(dep_port, arr_port, dep_date)

        if trips == []:

            print('No tickets match your requirements')

            continue

        print('--------------------------------------------------')

        if ret == 'y':
            
            ret_trips = searchTrips(arr_port, dep_port, ret_date)

            if ret_trips == []:

                print('No tickets match your requirements')

                continue


        print('--------------------------------------------\nINITIAL TRIP')
        for i in range(0,len(trips)):

            print('\n\nTRIP ' + str(i) + ':')
            print('Departure: ' + trips[i]['stations'][0][0] + ' at ' + trips[i]['stations'][0][2])

            for j in range(1,len(trips[i]['stations'])-1):

                print('Station ' + str(j) + ': ' + trips[i]['stations'][j][0] + ' at ' + trips[i]['stations'][j][2])
                
            print('Arrival: ' + trips[i]['stations'][-1][0] + ' at ' + trips[i]['stations'][-1][2])
            print('Base Cost: ' + str(trips[i]['base_cost']))


        if ret == 'y':
            
            print('--------------------------------------------\nRETURN TRIP')
            for i in range(0,len(ret_trips)):

                print('\n\nTRIP ' + str(i) + ':')
                print('Departure: ' + ret_trips[i]['stations'][0][0] + ' at ' + ret_trips[i]['stations'][0][2])

                for j in range(1,len(ret_trips[i]['stations'])-1):

                    print('Station ' + str(j) + ': ' + ret_trips[i]['stations'][j][0] + ' at ' + ret_trips[i]['stations'][j][2])
                    
                print('Arrival: ' + ret_trips[i]['stations'][-1][0] + ' at ' + ret_trips[i]['stations'][-1][2])
                print('Base Cost: ' + str(ret_trips[i]['base_cost']))



        ini_trip = int(input('\n\nSelect initial trip: '))

        if ret == 'y':
            
            ret_trip = int(input('Select return trip: '))


        tickets = []

        print('\n-----------------------------------------\n')
        print('INITIAL TRIP DETAILS')

        tickets += inTicketParams(trips[ini_trip])

        if ret == 'y':

            print('\n-----------------------------------------\n')
            print('RETURN TRIP DETAILS')
            
            tickets += inTicketParams(ret_trips[ret_trip])
        
####

        print('\n')

        tot_cost = 0
        
        for i in range(0,numofpas):
            
            print('\nPassenger ' + str(i+1) + '\n'
                  + dep_port + ' - ' + arr_port + ': ' + tickets[i]['info']['ticket_type'] + ', ' + tickets[i]['info']['ticket_class'])

            if tickets[i]['vehicle'] == 0:

                vehicle_type = None

            else:

                vehicle_type = tickets[i]['vehicle']['vehicle_type']

            x = dbf.getTicketTotalCost(tickets[i]['trip']['id'], tickets[i]['trip']['dep_rs'], tickets[i]['trip']['arr_rs'], tickets[i]['info']['ticket_type'],
                                       tickets[i]['info']['ticket_class'], vehicle_type)

            tickets[i]['final_cost'] = x[0][0]

            print('Cost of trip: ' + str(x[0][0]))

            tot_cost += x[0][0]

            if ret == 'y':
                
                print(arr_port + ' - ' + dep_port + ': ' + tickets[numofpas+i]['info']['ticket_type'] + ', ' + tickets[numofpas+i]['info']['ticket_class'])

                if tickets[numofpas+i]['vehicle'] == 0:

                    vehicle_type = None

                else:

                    vehicle_type = tickets[numofpas+i]['vehicle']['vehicle_type']

                x = dbf.getTicketTotalCost(tickets[numofpas+i]['trip']['id'], tickets[numofpas+i]['trip']['dep_rs'], tickets[numofpas+i]['trip']['arr_rs'],
                                           tickets[numofpas+i]['info']['ticket_type'], tickets[numofpas+i]['info']['ticket_class'], vehicle_type)

                tickets[numofpas+i]['final_cost'] = x[0][0]
                
                print('Cost of trip: ' + str(x[0][0]))

                tot_cost += x[0][0]


            

            tickets[i]['info']['fname'] = input('\nFirst Name: ')

            tickets[i]['info']['lname'] = input('Last Name: ')

            tickets[i]['info']['nat'] = input('Nationality (3 letter code): ')

            tickets[i]['info']['dob'] = input('Date Of Birth (YYYY/MM/DD): ')

            if ret == 'y':

                tickets[numofpas+i]['info']['fname'] = tickets[i]['info']['fname']

                tickets[numofpas+i]['info']['lname'] = tickets[i]['info']['lname']

                tickets[numofpas+i]['info']['nat'] = tickets[i]['info']['nat']

                tickets[numofpas+i]['info']['dob'] = tickets[i]['info']['dob']


            if tickets[i]['info']['ticket_type'] != 'Infant' and tickets[i]['info']['ticket_type'] != 'Child':

                tickets[i]['info']['email'] = input('Email: ')
                tickets[i]['info']['mob_phone'] = input('Mobile phone: ')
                tickets[i]['info']['nationalID'] = input('National ID number: ')

                if ret == 'y':

                    tickets[numofpas+i]['info']['email'] = tickets[i]['info']['email']
                    tickets[numofpas+i]['info']['mob_phone'] = tickets[i]['info']['mob_phone']
                    tickets[numofpas+i]['info']['nationalID'] = tickets[i]['info']['nationalID']

            else:

                tickets[i]['info']['email'] = None
                tickets[i]['info']['mob_phone'] = None
                tickets[i]['info']['nationalID'] = None

                if ret == 'y':

                    tickets[numofpas+i]['info']['email'] = None
                    tickets[numofpas+i]['info']['mob_phone'] = None
                    tickets[numofpas+i]['info']['nationalID'] = None
     

        
        print('\nThe total cost comes up to ' + str(tot_cost))

        while True:

            cpn = input('Coupon code (type no if you dont have one): ')

            if cpn == 'no':

                cpn = None
                
                break

            x = dbf.getCouponDiscount(cpn)

            if x == []:

                print('Coupon isnt valid. Please try again.')

                continue

            tot_cost = tot_cost - tot_cost * x[0][0]

            break
            

        ins = input('Travel Insurance (20 euro fee) (y/n): ')

        if ins == 'y':

            tot_cost += 20

            ins = 1

        else:

            ins = 0

        sms = input('SMS Notification (2.5 euro fee) (y/n): ')

        if sms == 'y':

            tot_cost += 2.5

            sms = 1

        else:

            sms = 0


        print('\nNew Total Cost comes up to: ' + str(tot_cost))
        
        if input('\nProceed to payment? (y/n)') == 'n': break

        print('''\n\nPayment Methods:\n
0. paypal
1. paysafe
2. visa
3. mastercard
4. bitcoin''')

        pm = input('\nPayment method: ')



        for ticket in tickets:

            obj1 = datetime.strptime(ticket['trip']['stations'][0][2], '%Y-%m-%d %H:%M:%S')

            obj2 = datetime.strptime(ticket['trip']['stations'][-1][2], '%Y-%m-%d %H:%M:%S')

            x = obj2 - obj1

            print('\n-------------------------------------------------------')

            print('Passenger: ' + ticket['info']['fname'] + ' ' + ticket['info']['lname'])
            print('Ticket code: ' + ticket['trip']['trip_info'][0])
            print('Departure: ' + ticket['trip']['stations'][0][2] +
                  ' from ' + ticket['trip']['stations'][0][0])
            print('Arrival: ' + ticket['trip']['stations'][-1][2] +
                  ' at ' + ticket['trip']['stations'][-1][0])
            print('Ship name: ' + ticket['trip']['trip_info'][1])
            print('Ship type: ' + ticket['trip']['trip_info'][2])
            print('Company name: ' + ticket['trip']['trip_info'][3])
            print('Ticket cost: ' + str(ticket['final_cost']))
            print('Vehicle: ' + str(ticket['vehicle']['vehicle_type']))

            print('-------------------------------------------------------\n')
            
            
            

        payment_id = dbf.storePayment(tot_cost, ins, sms, datetime.today().strftime('%Y-%m-%d'), pm, cpn)


        for ticket in tickets:

            if ticket['info']['ticket_class'] == 'Deck':

                ticket['info']['ticket_class'] = None


            passenger_id = dbf.getPassengerID(ticket['info']['nationalID'])

            if passenger_id == []:

                passenger_id = dbf.storePassenger(ticket['info']['fname'],
                                                  ticket['info']['lname'],
                                                  ticket['info']['nat'],
                                                  ticket['info']['mob_phone'],
                                                  ticket['info']['email'],
                                                  ticket['info']['dob'],
                                                  ticket['info']['nationalID'])

                passenger_id = int(passenger_id)
                
            else:
                
                passenger_id = int(passenger_id[0][0])

            x = dbf.getTripUID(ticket['trip']['id'])
            
            ticket_code = dbf.generateTicketCode(x[0][0],
                                             ticket['trip']['dep_rs'],
                                             ticket['trip']['arr_rs'],
                                             x[0][1],
                                             ticket['trip']['stations'][0][2])


            temp = dbf.getRouteID(ticket['trip']['id'],ticket['trip']['dep_rs'],ticket['trip']['arr_rs'])
            
            dbf.storeTicket(ticket_code,
                            ticket['final_cost'],
                            ticket['info']['ticket_class'],
                            ticket['vehicle']['vehicle_type'],
                            ticket['info']['ticket_type'],
                            payment_id,
                            passenger_id,
                            ticket['trip']['id'],
                            temp[0],
                            temp[1])


            x = ticket['vehicle']['vehicle_type']
            
            if x == 'Car':

                y = 2

            elif x == 'Motorcycle':

                y = 1

            elif x == 'Truck':

                y = 4

            else:

                y = 0

            dbf.updateSeatCapacity(ticket['trip']['id'],
                                   ticket['trip']['dep_rs'],
                                   ticket['trip']['arr_rs'],
                                   1,
                                   y)
































    
