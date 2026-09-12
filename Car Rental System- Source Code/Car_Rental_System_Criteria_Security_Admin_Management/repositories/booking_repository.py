class BookingRepository:
    def __init__(self, db): self.db=db

    def create(self,b):
        with self.db.get_connection() as conn:
            cur=conn.execute("""INSERT INTO bookings
                (car_id,customer_id,pickup_date,return_date,rental_days,daily_rate,
                 additional_charges,total_fee,customer_details,booking_status)
                VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (b.car_id,b.customer_id,b.pickup_date,b.return_date,b.rental_days,
                 b.daily_rate,b.additional_charges,b.total_fee,b.customer_details,b.booking_status))
            return cur.lastrowid

    def find(self, booking_id):
        with self.db.get_connection() as conn:
            return conn.execute("SELECT * FROM bookings WHERE booking_id=?",(booking_id,)).fetchone()

    def customer_bookings(self, customer_id):
        with self.db.get_connection() as conn:
            return conn.execute("""SELECT b.*,c.make,c.model,c.plate_number
                FROM bookings b JOIN cars c ON c.car_id=b.car_id
                WHERE b.customer_id=? ORDER BY b.booking_id DESC""",(customer_id,)).fetchall()

    def all(self):
        with self.db.get_connection() as conn:
            return conn.execute("""SELECT b.*,c.make,c.model,u.username,u.license_number
                FROM bookings b JOIN cars c ON c.car_id=b.car_id
                JOIN users u ON u.user_id=b.customer_id
                ORDER BY b.booking_id DESC""").fetchall()

    def update_status(self, booking_id, status):
        with self.db.get_connection() as conn:
            conn.execute("UPDATE bookings SET booking_status=? WHERE booking_id=?",(status,booking_id))

    def approved_active(self):
        with self.db.get_connection() as conn:
            return conn.execute("""SELECT b.*,u.license_number
                FROM bookings b JOIN users u ON u.user_id=b.customer_id
                WHERE b.booking_status='Approved'""").fetchall()
