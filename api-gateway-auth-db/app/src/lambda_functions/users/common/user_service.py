import json
import logging
import os

from user_db_actions import get_user
from user_validation import validate_user_login
from user_db_model import UserModel
from jwt_token_service import RequestModel, TokenService

location = "/common/user"
log = logging.getLogger(location)
loglevel = os.getenv("LOG_LEVEL")
log.setLevel('INFO')

if loglevel:
    log.setLevel(loglevel)


class UserService():
    def __init__(self, user: UserModel =None) -> None:
        self.user = user
        

    def login(self, event):
        if self.get_json_data("headers", event) is not None:
            headers = event["headers"]
            username = self.get_json_data("username", headers)
            password = self.get_json_data("password", headers)
            return self.login_user(username, password)
        else:
            log.warning(f'headers was not found in event')
        return None

    def login_user(self, username, password, application="application_one"):
    
        self.user = UserModel()
        user = get_user(username, application)
        user.is_valid = validate_user_login(username, password, application, user)
        self.user = user

        return user.is_valid

    
    def get_json_data(self, varname, parameter):

        log.info(f'getting json data: {parameter}')

        if varname in parameter:
            return parameter[varname]
        
        return None

    def generate_token(self, expires_in_seconds=360):
        
        if self.user is not None and self.user.is_valid:
            request = RequestModel()
            request.client_id = self.user.application
            request.email = self.user.email
            if self.user.scopes:
                
                if type(self.user.scopes) is str:
                    #print('is string')
                    request.scopes = self.user.scopes
                else:
                    try:                        
                        request.scopes = " ".join(self.user.scopes)
                    except:
                        request.scopes = self.user.scopes

            request.expires_in_seconds = expires_in_seconds
            request.user = f'{self.user.first_name} {self.user.last_name}'
            
            tokenService = TokenService()
            token = tokenService.encode_jwt_token(request)
            return token
            
        else:
            log.error('You must load and login with a user before attempting to generate a token')