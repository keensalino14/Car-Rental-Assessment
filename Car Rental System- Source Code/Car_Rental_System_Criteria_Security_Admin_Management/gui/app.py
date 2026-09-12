import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from models.models import Booking
from factories.car_factory import CarFactory

class CarRentalApp(tk.Tk):
    def __init__(self, services):
        super().__init__()
        self.services=services
        self.current_user=None
        self.title("Car Rental and Booking System")
        self.geometry("1250x760")
        self.login_screen()

    def clear(self):
        for w in self.winfo_children(): w.destroy()

    def login_screen(self):
        self.clear()
        f=ttk.Frame(self,padding=35); f.pack(expand=True)
        ttk.Label(f,text="Car Rental System",font=("Arial",24)).grid(row=0,column=0,columnspan=2,pady=15)
        ttk.Label(f,text="Username").grid(row=1,column=0,pady=6)
        self.luser=ttk.Entry(f); self.luser.grid(row=1,column=1,pady=6)
        ttk.Label(f,text="Password").grid(row=2,column=0,pady=6)
        self.lpass=ttk.Entry(f,show="*"); self.lpass.grid(row=2,column=1,pady=6)
        ttk.Button(f,text="Login",command=self.login).grid(row=3,column=0,columnspan=2,pady=10)
        ttk.Button(f,text="Register Customer",command=self.registration).grid(row=4,column=0,columnspan=2)
        ttk.Button(f,text="Load Demo Data",command=self.demo).grid(row=5,column=0,columnspan=2,pady=8)

    def demo(self):
        self.services["db"].seed_demo_data()
        messagebox.showinfo("Demo Accounts",
            "Admin: admin / admin123\nCustomer: customer / customer123")

    def login(self):
        u=self.services["auth"].login(self.luser.get().strip(),self.lpass.get())
        if not u:
            messagebox.showerror("Login","Invalid username or password.")
            return
        self.current_user=u
        self.dashboard()

    def registration(self):
        self.clear()
        f=ttk.Frame(self,padding=25); f.pack(expand=True)
        ttk.Label(f,text="Customer Registration",font=("Arial",20)).grid(row=0,column=0,columnspan=2,pady=10)
        self.reg={}
        names=["Username","Password","First Name","Last Name","Email","Contact Number","License Number"]
        for i,n in enumerate(names,1):
            ttk.Label(f,text=n).grid(row=i,column=0,sticky="e",pady=4)
            e=ttk.Entry(f,show="*" if n=="Password" else "")
            e.grid(row=i,column=1,pady=4); self.reg[n]=e
        ttk.Button(f,text="Register",command=self.register).grid(row=8,column=0,columnspan=2,pady=10)
        ttk.Button(f,text="Back to Login",command=self.login_screen).grid(row=9,column=0,columnspan=2)

    def register(self):
        try:
            data={k:v.get().strip() for k,v in self.reg.items()}
            if not data["Username"] or not data["Password"] or not data["First Name"] or not data["Last Name"]:
                raise ValueError("Username, password, first name and last name are required.")
            self.services["auth"].register_customer({
                "username":data["Username"],"password":data["Password"],
                "first_name":data["First Name"],"last_name":data["Last Name"],
                "email":data["Email"],"contact_number":data["Contact Number"],
                "license_number":data["License Number"]})
            messagebox.showinfo("Registration","Customer account created.")
            self.login_screen()
        except Exception as ex: messagebox.showerror("Registration",str(ex))

    def dashboard(self):
        self.clear()
        top=ttk.Frame(self,padding=10); top.pack(fill="x")
        role=self.current_user["role"].upper()
        ttk.Label(top,text=f"{self.current_user['first_name']} {self.current_user['last_name']} ({role})",
                  font=("Arial",16)).pack(side="left")
        ttk.Button(top,text="Logout",command=self.login_screen).pack(side="right")
        nb=ttk.Notebook(self); nb.pack(fill="both",expand=True,padx=10,pady=10)
        if self.current_user["role"]=="admin":
            self.admin_cars(nb); self.admin_bookings(nb); self.admin_users(nb); self.admin_security(nb)
        else:
            self.customer_cars(nb); self.customer_booking(nb); self.customer_bookings(nb); self.customer_return(nb)

    def admin_cars(self,nb):
        f=ttk.Frame(nb,padding=10); nb.add(f,text="Car Management")
        labels=["Car ID","Make","Model","Year","Mileage","Min Days","Max Days","Daily Rate"]
        self.ce={}
        for i,n in enumerate(labels):
            ttk.Label(f,text=n).grid(row=i,column=0,sticky="e",pady=3)
            self.ce[n]=ttk.Entry(f); self.ce[n].grid(row=i,column=1)
        ttk.Button(f,text="Add",command=self.car_add).grid(row=8,column=0)
        ttk.Button(f,text="Update Selected",command=self.car_update).grid(row=8,column=1)
        ttk.Button(f,text="Delete Selected",command=self.car_delete).grid(row=8,column=2)
        self.car_tree=ttk.Treeview(f,columns=("id","make","model","year","mileage","available","min","max","rate","security"),show="headings")
        for c in self.car_tree["columns"]: self.car_tree.heading(c,text=c.title())
        self.car_tree.grid(row=0,column=3,rowspan=10,padx=15,sticky="nsew")
        self.car_tree.bind("<<TreeviewSelect>>",self.select_car)
        self.refresh_car_tree()

    def select_car(self,_=None):
        item=self.car_tree.focus()
        if not item:return
        v=self.car_tree.item(item)["values"]
        names=["Car ID","Make","Model","Year","Mileage","Min Days","Max Days","Daily Rate"]
        for n,val in zip(names,v[:5]+v[6:9]):
            self.ce[n].delete(0,"end"); self.ce[n].insert(0,str(val))

    def car_add(self):
        try:
            e=self.ce; c=CarFactory.create_car(e["Car ID"].get(),e["Make"].get(),e["Model"].get(),
                e["Year"].get(),e["Mileage"].get(),e["Min Days"].get(),e["Max Days"].get(),e["Daily Rate"].get())
            self.services["car"].add(c); self.refresh_car_tree(); messagebox.showinfo("Car","Car added.")
        except Exception as ex: messagebox.showerror("Car",str(ex))

    def car_update(self):
        try:
            e=self.ce; c=CarFactory.create_car(e["Car ID"].get(),e["Make"].get(),e["Model"].get(),
                e["Year"].get(),e["Mileage"].get(),e["Min Days"].get(),e["Max Days"].get(),e["Daily Rate"].get())
            self.services["car"].update(c); self.refresh_car_tree(); messagebox.showinfo("Car","Car updated.")
        except Exception as ex: messagebox.showerror("Car",str(ex))

    def car_delete(self):
        try:
            cid=self.ce["Car ID"].get().strip()
            if messagebox.askyesno("Delete","Delete this car?"):
                self.services["car"].delete(cid); self.refresh_car_tree()
        except Exception as ex: messagebox.showerror("Car",str(ex))

    def refresh_car_tree(self):
        if not hasattr(self,"car_tree"):return
        self.car_tree.delete(*self.car_tree.get_children())
        for r in self.services["car"].all():
            self.car_tree.insert("", "end",values=(r["car_id"],r["make"],r["model"],r["year"],r["mileage"],
                "Yes" if r["available_now"] else "No",r["minimum_rent_period"],r["maximum_rent_period"],
                r["daily_rate"],r["security_status"]))

    def admin_bookings(self,nb):
        f=ttk.Frame(nb,padding=10); nb.add(f,text="Rental Management")
        ttk.Button(f,text="Approve Selected",command=lambda:self.booking_decision("Approved")).pack(side="left",padx=5)
        ttk.Button(f,text="Reject Selected",command=lambda:self.booking_decision("Rejected")).pack(side="left",padx=5)
        ttk.Button(f,text="Refresh",command=self.refresh_admin_bookings).pack(side="left",padx=5)
        self.abt=ttk.Treeview(f,columns=("id","customer","car","pickup","return","days","total","status"),show="headings")
        for c in self.abt["columns"]:self.abt.heading(c,text=c.title())
        self.abt.pack(fill="both",expand=True,pady=10); self.refresh_admin_bookings()

    def refresh_admin_bookings(self):
        if not hasattr(self,"abt"):return
        self.abt.delete(*self.abt.get_children())
        for r in self.services["booking_repo"].all():
            self.abt.insert("", "end",values=(r["booking_id"],r["username"],f"{r['make']} {r['model']}",
                r["pickup_date"],r["return_date"],r["rental_days"],r["total_fee"],r["booking_status"]))

    def booking_decision(self,status):
        item=self.abt.focus()
        if not item:return messagebox.showwarning("Booking","Select a booking first.")
        bid=int(self.abt.item(item)["values"][0])
        try:
            (self.services["rental"].approve(bid) if status=="Approved" else self.services["rental"].reject(bid))
            self.refresh_admin_bookings(); self.refresh_car_tree()
        except Exception as ex: messagebox.showerror("Booking",str(ex))

    def admin_users(self,nb):
        f=ttk.Frame(nb,padding=10); nb.add(f,text="User Management")

        form=ttk.LabelFrame(f,text="Create User",padding=10)
        form.pack(fill="x",pady=(0,10))
        self.uf={}
        names=["Username","Password","First Name","Last Name","Email","Contact Number","License Number"]
        for i,n in enumerate(names):
            ttk.Label(form,text=n).grid(row=i//4,column=(i%4)*2,sticky="e",padx=4,pady=4)
            self.uf[n]=ttk.Entry(form,width=18,show="*" if n=="Password" else "")
            self.uf[n].grid(row=i//4,column=(i%4)*2+1,padx=4,pady=4)

        ttk.Label(form,text="Role").grid(row=2,column=0,sticky="e",padx=4,pady=4)
        self.urole=ttk.Combobox(form,values=("customer","admin"),state="readonly",width=16)
        self.urole.set("customer"); self.urole.grid(row=2,column=1,padx=4,pady=4)

        ttk.Button(form,text="Create User",command=self.create_admin_user).grid(row=3,column=0,columnspan=2,pady=8)
        ttk.Button(form,text="Delete Selected",command=self.delete_admin_user).grid(row=3,column=2,columnspan=2,pady=8)
        ttk.Button(form,text="Refresh Users",command=self.refresh_users).grid(row=3,column=4,columnspan=2,pady=8)

        self.ut=ttk.Treeview(f,columns=("id","username","role","name","email","contact","license"),show="headings")
        for c in self.ut["columns"]: self.ut.heading(c,text=c.title())
        self.ut.pack(fill="both",expand=True)
        self.refresh_users()

    def create_admin_user(self):
        try:
            data={k:v.get().strip() for k,v in self.uf.items()}
            if not data["Username"] or not data["Password"] or not data["First Name"] or not data["Last Name"]:
                raise ValueError("Username, password, first name and last name are required.")
            data["role"]=self.urole.get()
            self.services["auth"].create_user(data)
            messagebox.showinfo("User Management",
                                f"{data['role'].title()} account '{data['Username']}' created.")
            for e in self.uf.values(): e.delete(0,"end")
            self.refresh_users()
        except Exception as ex:
            messagebox.showerror("User Management",str(ex))

    def refresh_users(self):
        if not hasattr(self,"ut"): return
        self.ut.delete(*self.ut.get_children())
        for u in self.services["auth"].all_users():
            self.ut.insert("", "end",values=(u["user_id"],u["username"],u["role"],
                f"{u['first_name']} {u['last_name']}",u["email"],u["contact_number"],u["license_number"]))

    def delete_admin_user(self):
        item=self.ut.focus()
        if not item:
            messagebox.showwarning("User Management","Select a user first.")
            return
        values=self.ut.item(item)["values"]
        user_id=int(values[0])
        username=str(values[1])
        if username==self.current_user["username"]:
            messagebox.showwarning("User Management","You cannot delete the account currently logged in.")
            return
        if messagebox.askyesno("Delete User",f"Delete user '{username}'?"):
            try:
                self.services["auth"].delete_user(user_id)
                self.refresh_users()
            except Exception as ex:
                messagebox.showerror("User Management",str(ex))

    def admin_security(self,nb):
        f=ttk.Frame(nb,padding=10); nb.add(f,text="Vehicle Security")
        ttk.Button(f,text="Run Security Check",command=self.security_check).pack(pady=5)
        self.sec=tk.Text(f,height=28); self.sec.pack(fill="both",expand=True)
        self.refresh_security()

    def security_check(self):
        result=self.services["security"].run_check()
        self.refresh_security()
        messagebox.showinfo("Security Check","\\n".join(result) if result else "No overdue vehicles found.")

    def refresh_security(self):
        if not hasattr(self,"sec"):return
        self.sec.delete("1.0","end")
        self.sec.insert("end","SECURITY ALERTS\\n")
        for r in self.services["security_repo"].alerts():
            self.sec.insert("end",f"Booking {r['booking_id']} | {r['alert_date']} | {r['message']}\\n")
        self.sec.insert("end","\\nTHEFT REPORTS\\n")
        for r in self.services["security_repo"].theft_reports():
            self.sec.insert("end",f"Report {r['report_id']} | Booking {r['booking_id']} | "
                                   f"License {r['license_number']} | {r['incident_type']} | {r['report_date']}\\n")

    def customer_cars(self,nb):
        f=ttk.Frame(nb,padding=10); nb.add(f,text="Available Cars")
        toolbar=ttk.Frame(f)
        toolbar.pack(fill="x",pady=(0,6))
        ttk.Button(toolbar,text="Refresh Cars",command=self.refresh_customer_cars).pack(side="left")
        self.car_loading=ttk.Label(toolbar,text="Ready")
        self.car_loading.pack(side="left",padx=10)

        self.cbt=ttk.Treeview(f,columns=("id","make","model","year","mileage","min","max","rate"),show="headings")
        for c in self.cbt["columns"]:self.cbt.heading(c,text=c.title())
        self.cbt.pack(fill="both",expand=True)
        # Load after the dashboard has rendered so the window appears immediately.
        self.after(50,self.refresh_customer_cars)

    def refresh_customer_cars(self):
        if not hasattr(self,"cbt"):return
        self.car_loading.config(text="Loading...")
        self.update_idletasks()

        rows=self.services["car"].available()
        values=[(r["car_id"],r["make"],r["model"],r["year"],r["mileage"],
                 r["minimum_rent_period"],r["maximum_rent_period"],r["daily_rate"]) for r in rows]

        self.cbt.delete(*self.cbt.get_children())
        for value in values:
            self.cbt.insert("", "end",values=value)

        self.car_loading.config(text=f"{len(values)} available car(s)")

    def customer_booking(self,nb):
        f=ttk.Frame(nb,padding=15); nb.add(f,text="Book a Car")
        labels=["Car ID","Pickup (YYYY-MM-DDTHH:MM)","Return (YYYY-MM-DDTHH:MM)","Additional Charges","Customer Details"]
        self.bf={}
        for i,n in enumerate(labels):
            ttk.Label(f,text=n).grid(row=i,column=0,sticky="e",pady=6)
            e=ttk.Entry(f,width=35);e.grid(row=i,column=1);self.bf[n]=e
        ttk.Button(f,text="Calculate & Submit Booking",command=self.create_booking).grid(row=5,column=0,columnspan=2,pady=12)

    def create_booking(self):
        try:
            e=self.bf; cid=e["Car ID"].get().strip()
            car=next((r for r in self.services["car"].available() if r["car_id"]==cid),None)
            if not car:raise ValueError("Car is not available.")
            pickup=e["Pickup (YYYY-MM-DDTHH:MM)"].get().strip()
            ret=e["Return (YYYY-MM-DDTHH:MM)"].get().strip()
            extra=float(e["Additional Charges"].get() or 0)
            days,total=self.services["booking"].calculate(pickup,ret,car,extra)
            b=Booking(None,cid,self.current_user["user_id"],pickup,ret,days,car["daily_rate"],
                      extra,total,e["Customer Details"].get().strip())
            bid=self.services["booking"].create(b)
            messagebox.showinfo("Booking",f"Booking #{bid} submitted for admin approval.\\nTotal fee: ${total:.2f}")
            self.after(50,self.refresh_customer_cars)
        except Exception as ex:messagebox.showerror("Booking",str(ex))

    def customer_bookings(self,nb):
        f=ttk.Frame(nb,padding=10); nb.add(f,text="My Bookings")
        self.mbt=ttk.Treeview(f,columns=("id","car","pickup","return","days","total","status"),show="headings")
        for c in self.mbt["columns"]:self.mbt.heading(c,text=c.title())
        self.mbt.pack(fill="both",expand=True); ttk.Button(f,text="Refresh",command=self.refresh_my_bookings).pack(pady=5)
        self.refresh_my_bookings()

    def refresh_my_bookings(self):
        if not hasattr(self,"mbt"):return
        self.mbt.delete(*self.mbt.get_children())
        for r in self.services["booking_repo"].customer_bookings(self.current_user["user_id"]):
            self.mbt.insert("", "end",values=(r["booking_id"],f"{r['make']} {r['model']}",r["pickup_date"],
                r["return_date"],r["rental_days"],r["total_fee"],r["booking_status"]))

    def customer_return(self,nb):
        f=ttk.Frame(nb,padding=15); nb.add(f,text="Car Return")
        ttk.Label(f,text="Approved/overdue Booking ID").grid(row=0,column=0,pady=8)
        self.return_id=ttk.Entry(f);self.return_id.grid(row=0,column=1)
        ttk.Button(f,text="Return Vehicle",command=self.return_vehicle).grid(row=1,column=0,columnspan=2,pady=10)

    def return_vehicle(self):
        try:
            bid=int(self.return_id.get())
            b=self.services["booking_repo"].find(bid)
            if not b or b["customer_id"]!=self.current_user["user_id"]:
                raise ValueError("Booking not found for this customer.")
            self.services["rental"].process_return(bid,self.services["return_repo"],self.services["security_repo"])
            messagebox.showinfo("Return","Vehicle return recorded.")
            self.refresh_my_bookings();self.refresh_customer_cars()
        except Exception as ex:messagebox.showerror("Return",str(ex))
