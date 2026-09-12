import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "car_rental.db"

class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self._initialized = True
        self.initialize_database()

    def get_connection(self):
        conn = sqlite3.connect(DB_PATH, timeout=5)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA busy_timeout = 5000")
        conn.execute("PRAGMA journal_mode = WAL")
        conn.execute("PRAGMA synchronous = NORMAL")
        return conn

    def initialize_database(self):
        with self.get_connection() as conn:
            conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('customer','admin')),
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT,
                contact_number TEXT,
                license_number TEXT
            );

            CREATE TABLE IF NOT EXISTS cars (
                car_id TEXT PRIMARY KEY,
                make TEXT NOT NULL,
                model TEXT NOT NULL,
                year INTEGER NOT NULL,
                mileage INTEGER NOT NULL DEFAULT 0,
                available_now INTEGER NOT NULL DEFAULT 1,
                minimum_rent_period INTEGER NOT NULL DEFAULT 1,
                maximum_rent_period INTEGER NOT NULL DEFAULT 30,
                daily_rate REAL NOT NULL,
                security_status TEXT NOT NULL DEFAULT 'Secure'
            );

            CREATE TABLE IF NOT EXISTS bookings (
                booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                car_id TEXT NOT NULL,
                customer_id INTEGER NOT NULL,
                pickup_date TEXT NOT NULL,
                return_date TEXT NOT NULL,
                rental_days INTEGER NOT NULL,
                daily_rate REAL NOT NULL,
                additional_charges REAL NOT NULL DEFAULT 0,
                total_fee REAL NOT NULL,
                customer_details TEXT,
                booking_status TEXT NOT NULL DEFAULT 'Pending',
                FOREIGN KEY(car_id) REFERENCES cars(car_id),
                FOREIGN KEY(customer_id) REFERENCES users(user_id)
            );

            CREATE TABLE IF NOT EXISTS payments (
                payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                booking_id INTEGER NOT NULL,
                payment_date TEXT NOT NULL,
                amount REAL NOT NULL,
                payment_method TEXT NOT NULL,
                payment_status TEXT NOT NULL,
                deposit_amount REAL NOT NULL DEFAULT 0,
                FOREIGN KEY(booking_id) REFERENCES bookings(booking_id)
            );

            CREATE TABLE IF NOT EXISTS car_returns (
                return_id INTEGER PRIMARY KEY AUTOINCREMENT,
                booking_id INTEGER NOT NULL,
                car_id TEXT NOT NULL,
                return_date TEXT NOT NULL,
                return_time TEXT NOT NULL,
                return_status TEXT NOT NULL,
                FOREIGN KEY(booking_id) REFERENCES bookings(booking_id),
                FOREIGN KEY(car_id) REFERENCES cars(car_id)
            );

            CREATE TABLE IF NOT EXISTS security_alerts (
                alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
                booking_id INTEGER NOT NULL,
                alert_date TEXT NOT NULL,
                message TEXT NOT NULL,
                acknowledged INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY(booking_id) REFERENCES bookings(booking_id)
            );

            CREATE TABLE IF NOT EXISTS theft_reports (
                report_id INTEGER PRIMARY KEY AUTOINCREMENT,
                booking_id INTEGER NOT NULL,
                license_number TEXT NOT NULL,
                security_status TEXT NOT NULL,
                incident_type TEXT NOT NULL,
                report_date TEXT NOT NULL,
                FOREIGN KEY(booking_id) REFERENCES bookings(booking_id)
            );
            CREATE INDEX IF NOT EXISTS idx_cars_available_security
                ON cars(available_now, security_status);
            CREATE INDEX IF NOT EXISTS idx_bookings_customer
                ON bookings(customer_id);
            CREATE INDEX IF NOT EXISTS idx_bookings_status_return
                ON bookings(booking_status, return_date);
            """)

    def seed_demo_data(self):
        with self.get_connection() as conn:
            conn.execute("""
                INSERT OR IGNORE INTO users
                (username,password,role,first_name,last_name,email,contact_number,license_number)
                VALUES (?,?,?,?,?,?,?,?)
            """, ("admin","admin123","admin","System","Administrator",
                  "admin@example.com","0210000000","ADMIN-LIC"))

            conn.execute("""
                INSERT OR IGNORE INTO users
                (username,password,role,first_name,last_name,email,contact_number,license_number)
                VALUES (?,?,?,?,?,?,?,?)
            """, ("customer","customer123","customer","Demo","Customer",
                  "customer@example.com","0211111111","LIC001"))

            cars = [
                ("CAR001","Toyota","Corolla",2023,12000,1,1,30,65.0,"Secure"),
                ("CAR002","Mazda","CX-5",2022,18000,1,2,30,85.0,"Secure"),
                ("CAR003","Honda","Civic",2024,7000,1,1,21,75.0,"Secure"),
                ("CAR004","Ford","Escape",2021,25000,1,2,45,90.0,"Secure")
            ]
            for car in cars:
                # Insert demo cars if missing.
                conn.execute("""INSERT OR IGNORE INTO cars
                    (car_id,make,model,year,mileage,available_now,
                     minimum_rent_period,maximum_rent_period,daily_rate,security_status)
                    VALUES (?,?,?,?,?,?,?,?,?,?)""", car)

            # Reset only the four demo cars so the demo always starts with
            # visible, available, secure vehicles.
            for car in cars:
                conn.execute("""UPDATE cars
                    SET make=?, model=?, year=?, mileage=?,
                        available_now=1, minimum_rent_period=?,
                        maximum_rent_period=?, daily_rate=?,
                        security_status='Secure'
                    WHERE car_id=?""",
                    (car[1],car[2],car[3],car[4],car[6],car[7],car[8],car[0]))
