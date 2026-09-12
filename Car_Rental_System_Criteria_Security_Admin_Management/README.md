# Car Rental System – Criteria + Vehicle Security

## Requirements
Python 3.9+; Tkinter and SQLite are included with standard Python.

## Run
Windows:
    python main.py

macOS/Linux:
    python3 main.py

Click **Load Demo Data**.

Demo accounts:
- Admin: username `admin`, password `admin123`
- Customer: username `customer`, password `customer123`

## Criteria implemented

### User Management
a. Customer registration and login are implemented.
b. Customer and admin roles are differentiated.
   - Customer: view cars, create bookings, view own bookings, return vehicle.
   - Admin: add/update/delete cars, approve/reject bookings, run security checks.

### Car Management
c. Cars store:
   - Car ID
   - Make
   - Model
   - Year
   - Mileage
   - Available Now
   - Minimum Rent Period
   - Maximum Rent Period
   - Daily Rate
   - Security Status
d. Admin can add, update and delete car records.

### Rental Booking
e. Customers can view available cars and their details.
f. Customers can select a car, specify rental dates and enter customer details.
g. Fees are calculated from daily rate × rental days + additional charges.
   The requested rental duration is validated against the car's minimum/maximum period.

### Rental Management
h. Admin can approve or reject pending rental requests.

## Additional Vehicle Security Feature
- More than 1 hour after the approved return time:
  - booking becomes Overdue
  - security alert is created
  - car security status becomes Security Alert
- At least 24 hours after the approved return time:
  - theft report is generated
  - incident type records possible theft/non-return
  - renter license number is stored
- Admin runs this through **Vehicle Security → Run Security Check**.
- Returning an overdue vehicle restores its security status to Secure.


## Performance improvements
The optimized version uses faster SQLite settings, database indexes for common searches, and delayed/non-blocking car-list rendering. Customers also have a **Refresh Cars** button so the list is only refreshed when needed.


### If Available Cars shows 0
Click **Load Demo Data** on the login screen before logging in. The four demo vehicles are restored to Available/Secure automatically each time demo data is loaded.


## Admin User Management
An existing administrator can open **User Management** and create either a customer or an admin account.
Only an authenticated admin can access this screen. A logged-in admin cannot delete their own account.

Example:
- Login as `admin / admin123`
- Open **User Management**
- Select role `admin`
- Enter the new administrator's details
- Click **Create User**
- Logout and log in using the new admin account
