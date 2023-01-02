import json
import requests
import logging
import os

log = logging.getLogger("users/login")
loglevel = os.getenv("LOG_LEVEL")
# default to info (normal default is warning)
log.setLevel('INFO')

if loglevel:
    log.setLevel(loglevel)

location = "/users/login"
def lambda_handler(event, context):
    
    event_info = f'{location}: {json.dumps(event, default=str)}'
    log.info(event_info)
    print(event_info)

    ip = get_ip_address(event=event)
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
            "location": ip.text.replace("\n", ""),
            "action": f'{success}',
            "error": f'{error}'
        }),
    }


def get_ip_address(event):    
    try:
        ip = requests.get("http://checkip.amazonaws.com/")
        return ip
    except requests.RequestException as e:
        # Send some context about this error to Lambda Logs
        print(e)
        log.error(f'error getting ip address {str(e)}')
        raise e


def login(event):
    if get_json_data("headers", event) is not None:
        headers = event["headers"]
        username = get_json_data("username", headers)
        password = get_json_data("password", headers)
        return login_user(username, password)
    else:
        log.warning(f'headers was not found in event')
    return None

def login_user(username, password):
    log.info(f'todo: {location}')

    log.info(f'username: {username}')
    log.info(f'password: {password}')

    if username == "awslambda" and password == "awspassword":
        log.info(f'login_user returning true')
        return True

    log.info(f'login_user returning false')
    return False

def get_json_data(varname, parameter):

    log.info(f'getting json data: {parameter}')

    if varname in parameter:
        return parameter[varname]
    
    return None