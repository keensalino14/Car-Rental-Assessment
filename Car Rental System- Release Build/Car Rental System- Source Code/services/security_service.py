from datetime import datetime

class SecurityService:
    """Additional vehicle-security feature for non-return and possible theft."""
    def __init__(self, booking_repo, security_repo, car_repo):
        self.bookings=booking_repo; self.security=security_repo; self.cars=car_repo

    def run_check(self):
        now=datetime.now()
        results=[]
        for b in self.bookings.approved_active():
            due=datetime.fromisoformat(b["return_date"])
            hours=(now-due).total_seconds()/3600
            if hours >= 24:
                self.bookings.update_status(b["booking_id"],"Overdue")
                self.cars.set_security(b["car_id"],"Security Alert")
                self.security.alert(b["booking_id"],now.isoformat(timespec="seconds"),
                                    "Vehicle has not been returned for at least 24 hours.")
                self.security.theft_report(
                    b["booking_id"],b["license_number"],"Security Alert",
                    "Possible Vehicle Theft / Non-Return",now.isoformat(timespec="seconds"))
                results.append(f"Booking {b['booking_id']}: theft report generated.")
            elif hours > 1:
                self.bookings.update_status(b["booking_id"],"Overdue")
                self.cars.set_security(b["car_id"],"Security Alert")
                self.security.alert(b["booking_id"],now.isoformat(timespec="seconds"),
                                    "Vehicle is more than 1 hour overdue.")
                results.append(f"Booking {b['booking_id']}: 1-hour non-return alert generated.")
        return results
