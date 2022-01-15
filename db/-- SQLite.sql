-- SQLite
select * from COUPON;


SELECT DISTINCT uid
FROM TRIP 
JOIN ROUTE on TRIP.id = ROUTE.trip_id
WHERE 
    TRIP.company_id = 13 AND 
    date(ROUTE.dep_date) >= '2022-01-03' AND
    date(ROUTE.dep_date) <= '2022-01-04';


SELECT TICKET.id, TICKET.ticket_code, TICKET.cost, TICKET.special_seat, TICKET.v_type, TICKET.t_type, TICKET.payment_id, TICKET.passenger_id, TICKET.trip_id
FROM COMPANY JOIN TRIP ON COMPANY.id=TRIP.company_id
JOIN TICKET ON TRIP.id=TICKET.trip_id
WHERE COMPANY.api_url='bailey-macdonald.net';

SELECT COUPON.discount
FROM COUPON
WHERE COUPON.code='QUOsS';
