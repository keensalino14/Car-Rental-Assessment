class ReturnRepository:
    def __init__(self, db): self.db=db
    def create(self, booking_id, car_id, date, time, status):
        with self.db.get_connection() as conn:
            conn.execute("""INSERT INTO car_returns
                (booking_id,car_id,return_date,return_time,return_status)
                VALUES (?,?,?,?,?)""",(booking_id,car_id,date,time,status))
