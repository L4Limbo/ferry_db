import functions as dbf
from datetime import datetime

def updatePassenger(fname,lname,country_code,phone_number,email,bdate,id_card):

    passenger_id = dbf.getPassengerID(id_card)

    if passenger_id == []:

        print('Passenger not found.')

        return

    dbf.updatePassenger(fname,lname,country_code,phone_number,email,bdate,id_card)

    print('\n\n Update succesful!\n')
    print('Passenger with ID card ' + id_card + ' updated details')
    print('First Name: ' + fname)
    print('Last Name: ' + lname)
    print('Country Code: ' + country_code)
    print('Phone Number: ' + phone_number)
    print('Email Address: ' + email)
    print('Birth Date: ' + phone_number)
    

def addExtraCapacity(trip_id, deck_extra, veh_extra, air_extra, dcab_extra, qcab_extra):
    
    dbf.addExtraCapacity(trip_id, deck_extra, veh_extra, air_extra, dcab_extra, qcab_extra)

    print('\nSeats Added.')


    
def readTicketsOfCompany(api_url):

    temp = dbf.readTicketsOfCompany(api_url)

    if temp == []:

        print('\nNo tickets found.')

        return

    for el in temp:
        
        print(el)


def readTicketsOfTrip(trip_uid):

    print('\nTickets of trip ' + str(trip_uid) + '\n')
    
    for ticket in dbf.readTicketsOfTrip(trip_uid):

        print(ticket)
        

def getTopTenDestinations():

    print('\nTop 10 Destination Ports\n')
    
    for dest in dbf.getTopTenDestinations():

        print(dest)


def getTopTenDepartures():

    print('\nTop 10 Departure Ports\n')

    for dest in dbf.getTopTenDepartures():

        print(dest)


def deletePayment(payment_id):

    cpt = dbf.cancelledPaymentTrips(payment_id)

    arr = []
    
    for el in cpt:

        arr.append(dbf.cancelledPaymentSeats(payment_id, el[0]))

        dbf.restoreRouteCap(el[0], arr[-1][1][1], arr[-1][2][1], arr[-1][0][1], arr[-1][3][1])

    dbf.deletePayment(payment_id)

    print('Payment succesfully deleted.')



def addTrip(uid, ship_name, ship_type, deck_cap, air_cap,
            dcab_cap, qcab_cap, company_id, routes):

    x = dbf.storeTrip(uid, ship_name, ship_type, deck_cap, air_cap,
            dcab_cap, qcab_cap, company_id, routes)

    print('\nTrip succesfully added.')


def getOwnerOfTicket(ticket_code):

    x = dbf.getPassengerLinkedToTicket(ticket_code)

    print(x)
    

print('<><><><><><><><><><><><><><><><><><>')
print('Welcome to the Admin Interface.')
print('''\nAvailable Commands:
1. updatePassenger(fname,lname,country_code,phone_number,email,bdate,id_card)
2. addExtraCapacity(trip_id, deck_extra, veh_extra, air_extra, dcab_extra, qcab_extra)
3. readTicketsOfCompany(api_url)
4. readTicketsOfTrip(trip_uid)
5. getTopTenDestinations()
6. getTopTenDepartures()
7. deletePayment(payment_id)
8. addTrip(uid, ship_name, ship_type, deck_cap, air_cap, dcab_cap, qcab_cap, company_id, routes)
9. getOwnerOfTicket(ticket_code)\n\n''')
