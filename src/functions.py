import db
import faker

fake = faker.Faker()

dbfile = "db/ferry.db"
db = db.DataModel(dbfile)

# READ FUNCTIONS FOR USER

def findPorts(dep_port, arr_port, date, admin_msg=False, msg=""):
    
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
    

def getTripCost(trip_id, first_route, last_route):
    trip_id = int(trip_id)
    first_route = int(first_route)
    last_route = int(last_route)
    return db.readData(f'''
        SELECT sum(ROUTE.cost) as trip_cost
        FROM ROUTE
        WHERE ROUTE.trip_id={trip_id} AND ROUTE.route_seq>={first_route} AND ROUTE.route_seq<={last_route}
    ''')[0][0]
    
def getTotalCap(trip_id, first_route, last_route):
    return db.readData(f''' 
        SELECT min(ROUTE.deck_cap) AS mincap
        FROM ROUTE
        WHERE ROUTE.trip_id = {trip_id} AND ROUTE.route_seq >= {first_route} AND ROUTE.route_seq <= {last_route}
    ''')
    
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

def getTotalVehicleCap(trip_id, first_route, last_route):
    return db.readData(f''' 
        SELECT min(ROUTE.v_cap) AS minvcap
        FROM ROUTE
        WHERE ROUTE.trip_id = {trip_id} AND ROUTE.route_seq >= {first_route} AND ROUTE.route_seq <= {last_route}
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
    

# CREATE FUNCTIONS FOR USER
def storePassenger(fname,lname,country_code,phone_number,email,bdate,id_card):
    params = (fname,lname,country_code,phone_number,email,bdate,id_card)
    return db.executeSQL("INSERT INTO PASSENGER (fname,lname,country_code,phone_number,email,birthdate,id_card) VALUES (?,?,?,?,?,?,?)", params)


def storePayment(total_cost,insurance, sms, payment_date, payment_method, coupon_code):
    params = (total_cost,insurance, sms, payment_date, payment_method, coupon_code)
    return db.executeSQL("INSERT INTO PAYMENT (total_cost, insurance, sms, payment_date, payment_method, coupon_code) VALUES (?,?,?,?,?,?)",params)

def storeTicket(ticket_code, cost, special_seat, v_type, t_type, payment_id, passenger_id, trip_id,first_route, last_route):
    params =(ticket_code, cost, special_seat, v_type, t_type, payment_id, passenger_id, trip_id,first_route, last_route)
    return db.executeSQL("INSERT INTO TICKET (ticket_code, cost, special_seat, v_type, t_type, payment_id, passenger_id, trip_id, first_route, last_route) VALUES (?,?,?,?,?,?,?,?,?,?)",params=params)

def getCouponDiscount(coupon):
    return db.readData(f"SELECT discount FROM COUPON WHERE COUPON.code='{coupon}'")

def getPassengerID(id_card):
    return db.readData(f"SELECT id FROM PASSENGER WHERE PASSENGER.id_card='{id_card}' AND PASSENGER.id_card IS NOT NULL")

# UPDATE FUNCTIONS FOR USER
def updateSeatCapacity(trip_id,first_route,last_route, deck_cap, v_cap):
    params = (deck_cap,v_cap,trip_id, first_route, last_route)
    return db.executeSQL("UPDATE ROUTE SET deck_cap=deck_cap-?, v_cap=v_cap-? WHERE trip_id=? AND route_seq>=? AND route_seq<=?",params)

def getCompanyTickets(api_url, api_psw, start_date, last_date, trip_id):
    pass



# Generated Ticket Code
def generateTicketCode(trip_uid,first_route,last_route,ship_name,date):
    code = ""
    code += ship_name.upper()[:2] + date[:4] + trip_uid[:4] + str(first_route) + str(last_route) + fake.ean(8)[:3]
    return code


def getTripUID(trip_id):
    return db.readData(f"SELECT uid, ship_name FROM TRIP WHERE TRIP.id='{trip_id}'")