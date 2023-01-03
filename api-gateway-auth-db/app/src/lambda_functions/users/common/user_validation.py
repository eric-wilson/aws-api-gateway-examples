import logging
from hash_algo import generate_hashed_password
from user_db_model import UserModel
location = "common/user_validation"
log = logging.getLogger(f"{location}")



log.setLevel('INFO')

def validate_user_login(username, password, application, db_user: UserModel):
    hashed = generate_hashed_password(username, password, application)
    
        
    if db_user is not None and hashed == db_user.hashed_password:
        return True
    
    return False