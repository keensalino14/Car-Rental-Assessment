from database.database_manager import DatabaseManager
from repositories.user_repository import UserRepository
from repositories.car_repository import CarRepository
from repositories.booking_repository import BookingRepository
from repositories.payment_repository import PaymentRepository
from repositories.return_repository import ReturnRepository
from repositories.security_repository import SecurityRepository

from services.auth_service import AuthService
from services.car_service import CarService
from services.booking_service import BookingService
from services.rental_service import RentalService
from services.payment_service import PaymentService
from services.security_service import SecurityService
from gui.app import CarRentalApp

def build_services():
    db=DatabaseManager()
    ur=UserRepository(db); cr=CarRepository(db); br=BookingRepository(db)
    pr=PaymentRepository(db); rr=ReturnRepository(db); sr=SecurityRepository(db)
    return {
        "db":db,
        "auth":AuthService(ur),
        "car":CarService(cr),
        "booking":BookingService(br,cr),
        "rental":RentalService(br,cr),
        "payment":PaymentService(pr),
        "security":SecurityService(br,sr,cr),
        "booking_repo":br,
        "return_repo":rr,
        "security_repo":sr
    }

if __name__=="__main__":
    CarRentalApp(build_services()).mainloop()
