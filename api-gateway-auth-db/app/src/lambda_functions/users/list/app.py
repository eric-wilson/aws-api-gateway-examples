import json
import logging
import os



location = "/users/list"
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
    
    # very basic call to list the users (uses scan ~ not performat for large datasets)

   
    return {
        "statusCode": 200,
        "body": json.dumps({
            "location": f"{location}",            
            "event": f'{event_info}'
        }),
    }








