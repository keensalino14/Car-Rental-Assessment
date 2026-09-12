from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    user_id: Optional[int]
    username: str
    password: str
    role: str
    first_name: str
    last_name: str
    email: str
    contact_number: str
    license_number: str

@dataclass
class Car:
    car_id: str
    make: str
    model: str
    year: int
    mileage: int
    available_now: int
    minimum_rent_period: int
    maximum_rent_period: int
    daily_rate: float
    security_status: str = "Secure"

@dataclass
class Booking:
    booking_id: Optional[int]
    car_id: str
    customer_id: int
    pickup_date: str
    return_date: str
    rental_days: int
    daily_rate: float
    additional_charges: float
    total_fee: float
    customer_details: str
    booking_status: str = "Pending"
