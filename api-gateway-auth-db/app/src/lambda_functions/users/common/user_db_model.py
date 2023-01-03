
class UserModel():
    def __init__(self) -> None:
        self.id = None
        self.email = None
        self.scopes = None
        self.password = None
        self.hashed_password = None
        self.first_name = None
        self.last_name = None
        self.is_valid = False
        self.application = None
    
    