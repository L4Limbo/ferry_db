import db
import faker

fake = faker.Faker()


dbfile = "ferry.db"
db = db.DataModel(dbfile)

# READ FUNCTIONS FOR USER

def findPorts(dep_port, arr_port, date):
    return db.readData(f''' 
        SELECT dep_r.trip_id, dep_r.route_seq as first_route , arr_r.route_seq as last_route
        from ROUTE as dep_r left join ROUTE as arr_r on dep_r.trip_id=arr_r.trip_id
        where dep_r.dep_port_id IN (
            SELECT PORT.id
            FROM PORT
            WHERE PORT.name='{dep_port}'
        ) 
        and arr_r.arr_port_id IN (
            SELECT PORT.id
            FROM PORT
            WHERE PORT.name='{arr_port}'
        )
        and dep_r.route_seq<=arr_r.route_seq
        and date(dep_r.dep_date)='{date}';
    ''')


def getRouteSeq(first_route, last_route):
    return db.readData(f''' 
        SELECT route_seq
        FROM ROUTE
        WHERE id={first_route} OR id={last_route}
        ORDER BY route_seq ASC
        ''')

##def retrieveSequence(first_route, last_route):
##
##    temp = getRouteSeq(first_route, last_route)
##
##    if len(temp)>1: return [x[0][0],x[1][0]]
##
##    else: return [x[0][0],x[0][0]]


def getRouteID(trip_id, first_route, last_route):

    temp = db.readData(f''' 
        SELECT route_seq, id
        FROM ROUTE
        WHERE trip_id={trip_id} AND (route_seq={first_route} OR route_seq={last_route})
        ORDER BY route_seq ASC
        ''')

    if len(temp)>1: return [temp[0][1],temp[1][1]]

    else: return [temp[0][1],temp[0][1]]


def getTotalCap(trip_id, first_route, last_route):
    return db.readData(f''' 
        SELECT min(ROUTE.deck_cap) AS mincap
        FROM ROUTE
        WHERE ROUTE.trip_id = {trip_id} AND ROUTE.route_seq >= {first_route} AND ROUTE.route_seq <= {last_route}          
    ''')

def getTotalVehicleCap(trip_id, first_route, last_route):
    return db.readData(f''' 
        SELECT min(ROUTE.v_cap) AS minvcap
        FROM ROUTE
        WHERE ROUTE.trip_id = {trip_id} AND ROUTE.route_seq >= {first_route} AND ROUTE.route_seq <= {last_route}          
    ''')
    
    
def getTripStations(trip_id, first_route, last_route):
    return db.readData(f''' 
        SELECT DISTINCT name, seq, dates
        FROM(
            SELECT ROUTE.dep_port_id, route_seq as seq, ROUTE.dep_date as dates
            FROM ROUTE
            WHERE ROUTE.trip_id={trip_id} AND ROUTE.route_seq>={first_route} AND ROUTE.route_seq<={last_route}
            UNION ALL
            SELECT ROUTE.arr_port_id, 'end' as seq, ROUTE.arr_date as dates
            FROM ROUTE
            WHERE ROUTE.trip_id={trip_id} AND ROUTE.route_seq={last_route}
        ) AS X
        JOIN PORT ON X.dep_port_id=PORT.id          
    ''')

def getTripInfo(trip_id):
    return db.readData(f''' 
        SELECT DISTINCT uid, ship_name, ship_type, api_url
        FROM TRIP JOIN COMPANY ON TRIP.company_id=COMPANY.id
        WHERE TRIP.id = {trip_id}         
    ''')
    

def getTripCost(trip_id, first_route, last_route):
    trip_id = int(trip_id)
    first_route = int(first_route)
    last_route = int(last_route)
    return db.readData(f'''
        SELECT sum(ROUTE.cost) as trip_cost
        FROM ROUTE
        WHERE ROUTE.trip_id={trip_id} AND ROUTE.route_seq>={first_route} AND ROUTE.route_seq<={last_route}
    ''')[0][0]
    

def getSpecialSeats(trip_id):
    return db.readData(f''' 
        SELECT count(*) AS number, TICKET.special_seat AS seat_type
        FROM TICKET
        WHERE TICKET.trip_id = {trip_id} AND seat_type IS NOT NULL
        GROUP BY seat_type
        UNION
        SELECT 0 AS number, SPECIAL_SEAT_TYPE.type AS seat_type
        FROM SPECIAL_SEAT_TYPE
        WHERE seat_type
            NOT IN (
            SELECT T.special_seat as seat_type
            FROM TICKET AS T
            WHERE T.trip_id={trip_id} AND seat_type IS NOT NULL)
        GROUP BY seat_type
        ORDER BY seat_type
    ''')
    
    
def getTripCapacity(trip_id):
    return db.readData(f''' 
        SELECT TRIP.air_cap, TRIP.dcab_cap, TRIP.qcab_cap
        FROM TRIP
        WHERE TRIP.id={trip_id}
    ''')
    
    
def getTicketTotalCost(trip_id, first_route, last_route, ticket_type, seat_type, v_type):
    return db.readData(f''' 
        SELECT sum(ROUTE.cost) + 
        coalesce(
            (
            SELECT SPECIAL_SEAT_TYPE.fee
            FROM SPECIAL_SEAT_TYPE
            WHERE SPECIAL_SEAT_TYPE.type='{seat_type}'
            )
            ,0)*sum(ROUTE.cost) +
        coalesce(
            (
            SELECT VEHICLE_TYPE.fee
            FROM VEHICLE_TYPE
            WHERE VEHICLE_TYPE.type='{v_type}'
            )
            ,0)*sum(ROUTE.cost) -
        coalesce(
            (
            SELECT TICKET_TYPE.discount
            FROM TICKET_TYPE
            WHERE TICKET_TYPE.type='{ticket_type}'
            )
            ,0)*sum(ROUTE.cost) as total_cost
        FROM ROUTE
        WHERE ROUTE.trip_id = {trip_id} AND ROUTE.route_seq>={first_route} AND ROUTE.route_seq<={last_route}
    ''')

def getCouponDiscount(coupon):

    return db.readData(f"SELECT discount FROM COUPON WHERE COUPON.code='{coupon}'")


def getPassengerID(id_card):

    return db.readData(f"SELECT id FROM PASSENGER WHERE PASSENGER.id_card='{id_card}' AND PASSENGER.id_card IS NOT NULL")
    

# CREATE FUNCTIONS FOR USER
def storePassenger(fname,lname,country_code,phone_number,email,bdate,id_card):
    params = (fname,lname,country_code,phone_number,email,bdate,id_card)
    return db.executeSQL("INSERT INTO PASSENGER (fname,lname,country_code,phone_number,email,birthdate,id_card) VALUES (?,?,?,?,?,?,?)", params)


def storePayment(total_cost,insurance, sms, payment_date, payment_method, coupon_code):
    params = (total_cost,insurance, sms, payment_date, payment_method, coupon_code)
    return db.executeSQL("INSERT INTO PAYMENT (total_cost, insurance, sms, payment_date, payment_method, coupon_code) VALUES (?,?,?,?,?,?)",params)

def storeTicket(ticket_code, cost, special_seat, v_type, t_type, payment_id, passenger_id, trip_id, first_route, last_route):
    params =(ticket_code, cost, special_seat, v_type, t_type, payment_id, passenger_id, trip_id, first_route, last_route)
    return db.executeSQL("INSERT INTO TICKET (ticket_code, cost, special_seat, v_type, t_type, payment_id, passenger_id, trip_id, first_route, last_route) VALUES (?,?,?,?,?,?,?,?,?,?)",params=params)


# UPDATE FUNCTIONS FOR USER
def updateSeatCapacity(trip_id,first_route,last_route, deck_cap, v_cap):
    params = (deck_cap,v_cap,trip_id, first_route, last_route)
    return db.executeSQL("UPDATE ROUTE SET deck_cap=deck_cap-?, v_cap=v_cap-? WHERE trip_id=? AND route_seq>=? AND route_seq<=?",params)


def addExtraCapacity(trip_id, deck_extra, veh_extra, air_extra, dcab_extra, qcab_extra):
    
    db.executeSQL("UPDATE ROUTE SET deck_cap=deck_cap+?, v_cap=v_cap+? WHERE trip_id=?",(deck_extra, veh_extra, trip_id))

    return db.executeSQL("UPDATE TRIP SET deck_cap=deck_cap+?, air_cap=air_cap+?, dcab_cap=dcab_cap+?, qcab_cap=qcab_cap+? WHERE trip_id=?",(deck_extra, air_extra, dcab_extra, qcab_extra, trip_id))
    
    





# Generated Ticket Code
def generateTicketCode(trip_uid,first_route,last_route,ship_name,date):
    code = ""
    code += ship_name.upper()[:2] + date[:4] + trip_uid[:4] + str(first_route) + str(last_route) + fake.ean(8)[:3]
    return code


def getTripUID(trip_id):

        return db.readData(f"SELECT uid, ship_name FROM TRIP WHERE TRIP.id='{trip_id}'")


## ADMIN SECTION


def updatePassenger(fname,lname,country_code,phone_number,email,bdate,id_card):

    params = (fname,lname,country_code,phone_number,email,bdate,id_card)
    return db.executeSQL("UPDATE PASSENGER SET fname=?, lname=?, country_code=?, phone_number=?, email=?, birthdate=? WHERE id_card=?;", params)



def readTicketsOfCompany(api_url):

    return db.readData(f'''SELECT TICKET.id, TICKET.ticket_code, TICKET.cost, TICKET.special_seat, TICKET.v_type, TICKET.t_type, TICKET.payment_id, TICKET.passenger_id, TICKET.trip_id
    FROM COMPANY JOIN TRIP ON COMPANY.id=TRIP.company_id
    JOIN TICKET ON TRIP.id=TICKET.trip_id
    WHERE COMPANY.api_url='{api_url}' ''')


def readTicketsOfTrip(trip_uid):

    return db.readData(f'''SELECT TICKET.id, TICKET.ticket_code, TICKET.cost, TICKET.special_seat, TICKET.v_type, TICKET.t_type, TICKET.payment_id, TICKET.passenger_id, TICKET.trip_id
    FROM TRIP JOIN TICKET ON TRIP.id=TICKET.trip_id
    WHERE TRIP.uid = '{trip_uid}' ''')



def getTopTenDestinations():

    return db.readData(f'''SELECT COUNT(*) AS NumOfTickets, PORT.name
    FROM TICKET JOIN ROUTE ON ROUTE.trip_id=TICKET.trip_id JOIN PORT ON ROUTE.arr_port_id=PORT.id
    WHERE TICKET.last_route=ROUTE.id
    GROUP BY PORT.name
    ORDER BY COUNT(*) DESC
    LIMIT 10 ''')

def getTopTenDepartures():

    return db.readData(f'''SELECT COUNT(*) AS NumOfTickets, PORT.name
    FROM TICKET JOIN ROUTE ON ROUTE.trip_id=TICKET.trip_id JOIN PORT ON ROUTE.arr_port_id=PORT.id
    WHERE TICKET.first_route=ROUTE.id
    GROUP BY PORT.name
    ORDER BY COUNT(*) DESC
    LIMIT 10 ''')


def cancelledPaymentSeats(payment_id, trip_id):

    return db.readData(f'''SELECT 'first_route',TICKET.first_route as num
    FROM TICKET
    WHERE TICKET.payment_id={payment_id} AND TICKET.trip_id={trip_id}
    UNION
    SELECT 'last_route',TICKET.last_route
    FROM TICKET
    WHERE TICKET.payment_id={payment_id} AND TICKET.trip_id={trip_id}
    UNION
    SELECT 'deckadd',count(*)
    FROM TICKET
    WHERE TICKET.payment_id={payment_id} AND TICKET.trip_id={trip_id}
    UNION
    SELECT 'vehadd',SUM(num)
    FROM (
            SELECT count(*) * 2 as num
            FROM TICKET
            WHERE TICKET.payment_id={payment_id} AND TICKET.v_type = 'Car' AND TICKET.trip_id={trip_id}
            UNION
            SELECT count(*) * 1 as num
            FROM TICKET
            WHERE TICKET.payment_id={payment_id} AND TICKET.v_type = 'Motorcycle' AND TICKET.trip_id={trip_id}
            UNION
            SELECT count(*) * 4 as num
            FROM TICKET
            WHERE TICKET.payment_id={payment_id} AND TICKET.v_type = 'Truck' AND TICKET.trip_id={trip_id}
    )
    ORDER BY 'first_route' ''')


def cancelledPaymentTrips(payment_id):

    return db.readData(f'''SELECT DISTINCT TICKET.trip_id
    FROM TICKET
    WHERE TICKET.payment_id={payment_id} ''')


def deletePayment(payment_id):

    return db.executeSQL(f"DELETE FROM PAYMENT WHERE id={payment_id};")


def restoreRouteCap(trip_id, first_route, last_route, deck_extra, veh_extra):
    
    return db.executeSQL("UPDATE ROUTE SET deck_cap=deck_cap+?, v_cap=v_cap+? WHERE trip_id=? AND route_seq>=? and route_seq<=?",(deck_extra, veh_extra, trip_id, first_route, last_route))



def storeTrip(uid, ship_name, ship_type, deck_cap, air_cap,
            dcab_cap, qcab_cap, company_id, routes):

    params = (uid, ship_name, ship_type, deck_cap, air_cap, dcab_cap, qcab_cap, company_id)
    trip_id = db.executeSQL("INSERT INTO TRIP (uid, ship_name, ship_type, deck_cap, air_cap, dcab_cap, qcab_cap, company_id) VALUES (?,?,?,?,?,?,?,?)",params)

    for el in routes:

        params = el + (trip_id,)

        db.executeSQL("INSERT INTO ROUTE (cost, deck_cap, v_cap, dep_date, arr_date, route_seq, dep_port_id, arr_port_id, trip_id) VALUES (?,?,?,?,?,?,?,?,?)",params)
        

def deleteTrip(uid):

    deletedTickets = db.readData(f'''SELECT TICKET.ticket_code, PASSENGER.fname, PASSENGER.lname, PASSENGER.phone_number, PASSENGER.email,
    PAYMENT.payment_date, PAYMENT.total_cost, PAYMENT.payment_method, PAYMENT.coupon_code, COMPANY.api_url
    FROM TRIP JOIN TICKET ON TRIP.id=TICKET.trip_id
    JOIN PASSENGER ON TICKET.passenger_id=PASSENGER.id
    JOIN PAYMENT ON TICKET.payment_id = PAYMENT.id
    JOIN COMPANY ON TRIP.company_id=COMPANY.id
    WHERE TRIP.uid='{uid}' ''')
    
    db.executeSQL(f"DELETE FROM TRIP WHERE uid='{uid}';")

    deletedPayments = db.readData(f'''SELECT PAYMENT.id
    FROM TRIP JOIN TICKET ON TRIP.id=TICKET.trip_id
    JOIN PAYMENT ON TICKET.payment_id=PAYMENT.id
    WHERE TRIP.uid='{uid}' ''')


    for el in deletedPayments:

        pay_id = int(el[0])
        
        db.executeSQL(f"DELETE FROM PAYMENT WHERE id={pay_id};")

    return deletedTickets
    

    

def getPassengerLinkedToTicket(ticket_code):

    temp = db.readData(f'''SELECT TICKET.ticket_code, TICKET.cost,
    PASSENGER.fname, PASSENGER.lname, PASSENGER.id_card, PASSENGER.email, PASSENGER.phone_number,
    DEP.name, ARR.name
    FROM TICKET JOIN PASSENGER ON TICKET.passenger_id=PASSENGER.id
    JOIN ROUTE ON TICKET.first_route = ROUTE.id
    JOIN PORT AS DEP ON ROUTE.dep_port_id = DEP.id
    JOIN ROUTE AS R ON TICKET.last_route = R.id
    JOIN PORT AS ARR ON R.arr_port_id = ARR.id
    WHERE TICKET.ticket_code='{ticket_code}' ''')

    return temp
    




    

    






