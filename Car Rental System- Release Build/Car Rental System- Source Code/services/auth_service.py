from models.models import User

class AuthService:
    def __init__(self, repo): self.repo=repo

    def register_customer(self, data):
        return self.repo.register(User(
            None,data["username"],data["password"],"customer",
            data["first_name"],data["last_name"],data["email"],
            data["contact_number"],data["license_number"]))

    def create_user(self, data):
        role=data["role"].lower()
        if role not in ("customer","admin"):
            raise ValueError("Role must be customer or admin.")
        return self.repo.register(User(
            None,data["username"],data["password"],role,
            data["first_name"],data["last_name"],data["email"],
            data["contact_number"],data["license_number"]))

    def login(self, username, password):
        return self.repo.login(username,password)

    def all_users(self):
        return self.repo.all_users()

    def delete_user(self,user_id):
        self.repo.delete_user(user_id)
