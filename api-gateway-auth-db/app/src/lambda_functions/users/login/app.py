import json
import logging
import os

try:

    
    from common.user_service import UserService    
except:
        
    from user_service import UserService

location = "/users/login"
log = logging.getLogger(location)
loglevel = os.getenv("LOG_LEVEL")
# default to info (normal default is warning)
log.setLevel('INFO')
TOKEN_EXPIRE = os.getenv("JWT_TOKEN_EXPIRE")
if TOKEN_EXPIRE is None:
    TOKEN_EXPIRE = 60 * 60 * 3

if loglevel:
    log.setLevel(loglevel)


def lambda_handler(event, context):
    
    event_info = f'{location}: {json.dumps(event, default=str)}'
    log.info(event_info)
    print(event_info)
    
    success = False
    error = None
    token = None

    userService = UserService()

    try:
        
        if userService.login(event):
            success = True
            token = userService.generate_token(TOKEN_EXPIRE)

    except Exception as e:
        error = f"{str(e)}"
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"{location}",            
            "login": f'{success}',
            "error": f'{error}',
            "token": f'{token}'
        }),
    }

