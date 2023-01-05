import json
import logging
import os

try:    
    from common.jwt_token_service import TokenService    
except:
        
    from jwt_token_service import TokenService

location = "/authentication/authorizer"
log = logging.getLogger(location)
loglevel = os.getenv("LOG_LEVEL")
# default to info (normal default is warning)
log.setLevel('INFO')

if loglevel:
    log.setLevel(loglevel)


def lambda_handler(event, context):
    
    #event_info = f'{location}: {json.dumps(event, default=str)}'
    #log.info(event_info)
    #print(event_info)
    
    
    # try:
    #     event_info = f'{location}: {json.dumps(event, default=str)}'
    #     log.info(event_info)
    #     print(event_info)
        
    #     #return 200
    # except Exception as e:
    #     print(str(e))
    
    is_authorized = is_token_valid(event)
    
    response = {
            "isAuthorized": is_authorized,
            "context": {
                "stringKey": "value",
                "numberKey": 1,
                "booleanKey": True,
                "arrayKey": ["value1", "value2"],
                "mapKey": {"value1": "value2"}
            }
        }
    
    return response


def is_token_valid(event):
    if "headers" in event:
        #print('found headers')
        if "authorization" in event["headers"]:
            #print('found authorization')
            encoded = event["headers"]["authorization"]
            ts = TokenService()
            try:
                encoded = str(encoded).removeprefix("Bearer").strip()
                decoded = ts.verify_jwt_token(encoded)
                print(f'decoded: {decoded}')
                return True
            except Exception as e:
                print(f' failed to decoded token {str(e)}')
    else:
        print('no headers')
    
    
    return False
        
