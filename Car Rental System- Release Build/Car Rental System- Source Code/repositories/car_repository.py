class CarRepository:
    def __init__(self, db): self.db = db

    def add(self, car):
        with self.db.get_connection() as conn:
            conn.execute("""INSERT INTO cars
                (car_id,make,model,year,mileage,available_now,minimum_rent_period,
                 maximum_rent_period,daily_rate,security_status)
                VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (car.car_id,car.make,car.model,car.year,car.mileage,car.available_now,
                 car.minimum_rent_period,car.maximum_rent_period,car.daily_rate,car.security_status))

    def update(self, car):
        with self.db.get_connection() as conn:
            conn.execute("""UPDATE cars SET make=?,model=?,year=?,mileage=?,
                minimum_rent_period=?,maximum_rent_period=?,daily_rate=?
                WHERE car_id=?""",
                (car.make,car.model,car.year,car.mileage,car.minimum_rent_period,
                 car.maximum_rent_period,car.daily_rate,car.car_id))

    def delete(self, car_id):
        with self.db.get_connection() as conn:
            conn.execute("DELETE FROM cars WHERE car_id=?", (car_id,))

    def all(self):
        with self.db.get_connection() as conn:
            return conn.execute("SELECT * FROM cars ORDER BY car_id").fetchall()

    def available(self):
        with self.db.get_connection() as conn:
            return conn.execute("""SELECT * FROM cars
                WHERE available_now=1
                  AND (security_status='Secure' OR security_status IS NULL OR security_status='')
                ORDER BY car_id""").fetchall()

    def set_availability(self, car_id, value):
        with self.db.get_connection() as conn:
            conn.execute("UPDATE cars SET available_now=? WHERE car_id=?",(value,car_id))

    def set_security(self, car_id, status):
        with self.db.get_connection() as conn:
            conn.execute("UPDATE cars SET security_status=? WHERE car_id=?",(status,car_id))
