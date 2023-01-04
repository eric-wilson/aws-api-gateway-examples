import json
import logging
import os



location = "/authentication/authorizer"
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
    
   
    try:
        event_info = f'{location}: {json.dumps(event, default=str)}'
        log.info(event_info)
        print(event_info)
        
        #return 200
    except Exception as e:
        print(str(e))
        
    
    response = {
            "isAuthorized": True,
            "context": {
                "stringKey": "value",
                "numberKey": 1,
                "booleanKey": True,
                "arrayKey": ["value1", "value2"],
                "mapKey": {"value1": "value2"}
            }
        }
    
    return response
   
    return {
        "statusCode": 200,
        "body": json.dumps({
            "location": f"{location}",            
            "event": f'{event_info}'
        }),
    }








