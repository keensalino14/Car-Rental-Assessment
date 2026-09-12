class UserRepository:
    def __init__(self, db): self.db=db

    def register(self, user):
        with self.db.get_connection() as conn:
            cur=conn.execute("""
                INSERT INTO users
                (username,password,role,first_name,last_name,email,contact_number,license_number)
                VALUES (?,?,?,?,?,?,?,?)
            """,(user.username,user.password,user.role,user.first_name,user.last_name,
                 user.email,user.contact_number,user.license_number))
            return cur.lastrowid

    def login(self, username, password):
        with self.db.get_connection() as conn:
            return conn.execute(
                "SELECT * FROM users WHERE username=? AND password=?",
                (username,password)).fetchone()

    def all_users(self):
        with self.db.get_connection() as conn:
            return conn.execute("""SELECT user_id,username,role,first_name,last_name,
                email,contact_number,license_number FROM users ORDER BY user_id""").fetchall()

    def delete_user(self, user_id):
        with self.db.get_connection() as conn:
            conn.execute("DELETE FROM users WHERE user_id=?",(user_id,))
