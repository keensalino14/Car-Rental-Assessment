class PaymentRepository:
    def __init__(self, db): self.db=db
    def create(self, booking_id, date, amount, method, status, deposit):
        with self.db.get_connection() as conn:
            conn.execute("""INSERT INTO payments
                (booking_id,payment_date,amount,payment_method,payment_status,deposit_amount)
                VALUES (?,?,?,?,?,?)""",(booking_id,date,amount,method,status,deposit))
