from models.models import Car

class CarFactory:
    @classmethod
    def create_car(cls, car_id, make, model, year, mileage,
                   minimum_period, maximum_period, daily_rate):
        minimum_period = int(minimum_period)
        maximum_period = int(maximum_period)
        if minimum_period < 1:
            raise ValueError("Minimum rent period must be at least 1 day.")
        if maximum_period < minimum_period:
            raise ValueError("Maximum rent period must be greater than or equal to minimum.")
        return Car(
            car_id, make, model, int(year), int(mileage), 1,
            minimum_period, maximum_period, float(daily_rate), "Secure"
        )
