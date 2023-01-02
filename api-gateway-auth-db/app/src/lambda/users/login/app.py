import json
import logging
import os

try:

    from common.user_db_actions import validate_user_login
except:
    
    from user_db_actions import validate_user_login

location = "/users/login"
log = logging.getLogger(location)
loglevel = os.getenv("LOG_LEVEL")
# default to info (normal default is warning)
log.setLevel('INFO')

if loglevel:
    log.setLevel(loglevel)


def lambda_handler(event, context):
    
    event_info = f'{location}: {json.dumps(event, default=str)}'
    log.info(event_info)
    print(event_info)
    
    success = False
    error = None
    try:
        success = login(event)
    except Exception as e:
        error = f"{str(e)}"
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"{location}",            
            "action": f'{success}',
            "error": f'{error}'
        }),
    }


def login(event):
    if get_json_data("headers", event) is not None:
        headers = event["headers"]
        username = get_json_data("username", headers)
        password = get_json_data("password", headers)
        return login_user(username, password)
    else:
        log.warning(f'headers was not found in event')
    return None

def login_user(username, password, application="application_one"):
    log.info(f'todo: {location}')

    log.info(f'username: {username}')
    log.info(f'password: {password}')


    valid = validate_user_login(username, password, application)


    return valid

def get_json_data(varname, parameter):

    log.info(f'getting json data: {parameter}')

    if varname in parameter:
        return parameter[varname]
    
    return None