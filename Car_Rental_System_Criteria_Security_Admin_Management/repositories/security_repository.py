class SecurityRepository:
    def __init__(self, db): self.db=db

    def alert(self,bid,date,message):
        with self.db.get_connection() as conn:
            if not conn.execute("""SELECT 1 FROM security_alerts
                WHERE booking_id=? AND acknowledged=0""",(bid,)).fetchone():
                conn.execute("""INSERT INTO security_alerts
                    (booking_id,alert_date,message) VALUES (?,?,?)""",(bid,date,message))

    def theft_report(self,bid,license_number,status,incident,date):
        with self.db.get_connection() as conn:
            if not conn.execute("SELECT 1 FROM theft_reports WHERE booking_id=?",(bid,)).fetchone():
                conn.execute("""INSERT INTO theft_reports
                    (booking_id,license_number,security_status,incident_type,report_date)
                    VALUES (?,?,?,?,?)""",(bid,license_number,status,incident,date))

    def alerts(self):
        with self.db.get_connection() as conn:
            return conn.execute("""SELECT * FROM security_alerts
                WHERE acknowledged=0 ORDER BY alert_date DESC""").fetchall()

    def theft_reports(self):
        with self.db.get_connection() as conn:
            return conn.execute("""SELECT * FROM theft_reports
                ORDER BY report_date DESC""").fetchall()
