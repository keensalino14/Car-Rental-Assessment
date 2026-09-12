from datetime import datetime

class RentalService:
    def __init__(self, booking_repo, car_repo):
        self.bookings=booking_repo; self.cars=car_repo

    def approve(self, booking_id):
        b=self.bookings.find(booking_id)
        if not b: raise ValueError("Booking not found.")
        if b["booking_status"] != "Pending": raise ValueError("Only pending bookings can be approved.")
        self.bookings.update_status(booking_id,"Approved")
        self.cars.set_availability(b["car_id"],0)

    def reject(self, booking_id):
        b=self.bookings.find(booking_id)
        if not b: raise ValueError("Booking not found.")
        if b["booking_status"] != "Pending": raise ValueError("Only pending bookings can be rejected.")
        self.bookings.update_status(booking_id,"Rejected")
        self.cars.set_availability(b["car_id"],1)

    def process_return(self, booking_id, return_repo, security_repo):
        b=self.bookings.find(booking_id)
        if not b: raise ValueError("Booking not found.")
        if b["booking_status"] not in ("Approved","Overdue"):
            raise ValueError("Only approved/overdue rentals can be returned.")
        now=datetime.now()
        return_repo.create(booking_id,b["car_id"],now.date().isoformat(),
                           now.strftime("%H:%M:%S"),"Returned")
        self.bookings.update_status(booking_id,"Returned")
        self.cars.set_availability(b["car_id"],1)
        self.cars.set_security(b["car_id"],"Secure")
