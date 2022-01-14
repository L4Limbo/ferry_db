tt = ['Adult', 'Infant', 'Child', 'Student', 'Senior',
      'Passenger with reduced mobility', 'Greek military personel']

tc = ['Deck', 'Assigned Seat', '2 Bed Cabin (Single Bed)', '2 Bed Cabin (Whole Bed)',
      '4 Bed Cabin (Single Bed)', '4 Bed Cabin (Whole Bed)']

vt = ['Car', 'Motorcycle', 'Truck']

############################################################################################
############################################################################################

def inTicketParams(dep_port, arr_port):

    tickets = []
    
    print('''\nChoose a ticket type and a seat class for each passenger.
\nTicket types:
0. Adult
1. Infant
2. Child
3. Student
4. Senior
5. Passenger with reduced mobility
6. Greek military personel\n
Ticket classes:
0. Deck
1. Assigned Seat
2. 2 Bed Cabin (Single Bed)
3. 2 Bed Cabin (Whole Bed)
4. 4 Bed Cabin (Single Bed)
5. 4 Bed Cabin (Whole Bed)\n''')
        
    for i in range(0,numofpas):

        route = {}
        info = {}
        ticket = {}
        
        info['ticket_type'] = tt[int(input('Passenger ' + str(i+1) + ' ticket type: '))]

        info['ticket_class'] = tc[int(input('Passenger ' + str(i+1) + ' ticket class: '))]

        ticket['info'] = info

        route['dep_port'] = dep_port

        route['arr_port'] = arr_port

        ticket['route'] = route
        
        ticket['route']

        ticket['vehicle'] = 0

        tickets.append(ticket)


    print('''\nChoose a vehicle type for each vehicle.
Vehicle types:
0. Car
1. Motorcycle
2. Truck''')


    for i in range(0,numofveh):

        while True:

            p = int(input('\nVehicle ' + str(i+1) + ' is assigned to passenger: '))
            
            if tickets[p-1]['vehicle'] == 0 and tickets[p-1]['info']['ticket_type']!='Infant' and tickets[p-1]['info']['ticket_type']!='Child':

                tickets[p-1]['vehicle']={'vehicle_type' : vt[int(input('Vehicle ' + str(i+1) + ' type: '))]}

                break

            else:

                print('''Passenger has already been assigned a vehicle or cannot be assigned one.
Please try again''')


    return tickets
    
############################################################################################
############################################################################################

while True:
    
    x = input('''<><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
Welcome to the ProjectFerry app!
Type \'book\' to search for tickets\n''')

    if x == 'book':

        dep_port = input('\nDeparture port: ')

        arr_port = input('Arrival port: ')

        ret = input('Round trip? (y/n): ')

        dep_date = input('Departure date (YYYY/MM/DD): ')

        if ret == 'y':

            ret_date = input('Return date (YYYY/MM/DD): ')

        numofpas = int(input('Number of passengers: '))

        numofveh = int(input('Number of vehicles: '))

####

        tickets = []
        
        print('\nTRIP: ' + dep_port + ' - ' + arr_port)

        tickets += inTicketParams(dep_port, arr_port)

        if ret == 'y':
            
            tickets += inTicketParams(arr_port, dep_port)

####

        print('\n')
        
        for i in range(0,numofpas):
            
            print('\nPassenger ' + str(i+1) + '\n'
                  + dep_port + ' - ' + arr_port + ': ' + tickets[i]['info']['ticket_type'] + ', ' + tickets[i]['info']['ticket_class'])

            if ret == 'y':
                
                print(dep_port + ' - ' + arr_port + ': ' + tickets[numofpas+i]['info']['ticket_type'] + ', ' + tickets[numofpas+i]['info']['ticket_class'])
            

            tickets[i]['info']['fname'] = input('\nFirst Name: ')

            tickets[i]['info']['lname'] = input('Last Name: ')

            tickets[i]['info']['nat'] = input('Nationality (3 letter code): ')

            tickets[i]['info']['dob'] = input('Date Of Birth (YYYY/MM/DD): ')

            if ret == 'y':

                tickets[numofpas+i]['info']['fname'] = input('\nFirst Name: ')

                tickets[numofpas+i]['info']['lname'] = input('Last Name: ')

                tickets[numofpas+i]['info']['nat'] = input('Nationality (3 letter code): ')

                tickets[numofpas+i]['info']['dob'] = input('Date Of Birth (YYYY/MM/DD): ')


            if tickets[i]['info']['ticket_type'] != 'Infant' and tickets[i]['info']['ticket_type'] != 'Child':

                tickets[i]['info']['email'] = input('Email: ')
                tickets[i]['info']['mob_phone'] = input('Mobile phone: ')
                tickets[i]['info']['nationalID'] = input('National ID number: ')

                if ret == 'y':

                    tickets[numofpas+i]['info']['email'] = input('Email: ')
                    tickets[numofpas+i]['info']['mob_phone'] = input('Mobile phone: ')
                    tickets[numofpas+i]['info']['nationalID'] = input('National ID number: ')

                    
        for i in range(0,len(tickets)):

            if tickets[i]['vehicle']!=0:

                print('\nVehicle assigned to ' + tickets[i]['info']['fname'] + ' ' + tickets[i]['info']['lname'] + ' on route from ' + tickets[i]['route']['dep_port'] + ' to ' +
                      tickets[i]['route']['arr_port'])

                tickets[i]['vehicle']['platenum'] = input('License plate number: ')      

        
        print('\nThe total cost comes up to *price*')

        cpn = input('Coupon code: (type no if you dont have one)')

        ins = input('Insurance number: ')

        sms = input('SMS: ')


