import json
import logging
import os


try:    
    from common.user_service import UserService    
except:
        
    from user_service import UserService

location = "/users/list"
log = logging.getLogger(location)
loglevel = os.getenv("LOG_LEVEL")
# default to info (normal default is warning)
log.setLevel('INFO')

log.info('cold start')

if loglevel:
    log.setLevel(loglevel)


def lambda_handler(event, context):
    
    errors = None
    response = None
    try:
        event_info = f'{location}: {json.dumps(event, default=str)}'
        log.info(event_info)
        print(event_info)
        
        us = UserService()
        response = us.get_users()
        # very basic call to list the users (uses scan ~ not performat for large datasets)
    except Exception as e:
        log.error(str(e))
        errors = str(e)
   
    return {
        "statusCode": 200,
        "body": json.dumps({
            "location": f"{location}",            
            #"event": f'{event_info}',
            "users": response,
            "errors": errors
        }),
    }








