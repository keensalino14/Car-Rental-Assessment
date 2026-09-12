from datetime import datetime
import math

class BookingService:
    def __init__(self, repo, car_repo):
        self.repo=repo; self.car_repo=car_repo

    def calculate(self, pickup, return_date, car, additional_charges):
        start=datetime.fromisoformat(pickup)
        end=datetime.fromisoformat(return_date)
        if end <= start:
            raise ValueError("Return date must be after pickup date.")
        days=max(1,math.ceil((end-start).total_seconds()/86400))
        if days < car["minimum_rent_period"] or days > car["maximum_rent_period"]:
            raise ValueError(
                f"Rental period must be between {car['minimum_rent_period']} "
                f"and {car['maximum_rent_period']} days."
            )
        extra=float(additional_charges or 0)
        total=round(days*float(car["daily_rate"])+extra,2)
        return days,total

    def create(self,b):
        booking_id=self.repo.create(b)
        # A car is reserved while its booking awaits admin decision.
        self.car_repo.set_availability(b.car_id,0)
        return booking_id
