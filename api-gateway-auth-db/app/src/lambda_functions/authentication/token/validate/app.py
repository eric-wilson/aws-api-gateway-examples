import json
import logging
import os

try:    
    from common.jwt_token_service import TokenService    
except:
        
    from jwt_token_service import TokenService

location = "/authentication/token/validate"
log = logging.getLogger(location)
loglevel = os.getenv("LOG_LEVEL")
# default to info (normal default is warning)
log.setLevel('INFO')

if loglevel:
    log.setLevel(loglevel)


def lambda_handler(event, context):
    
    error = None
    message = None

    try:
        message = valdiate_token(event)
    except Exception as e:
        error = str(e)
    
    response = {
        "statusCode": 200,
        "body": json.dumps({
            "location": f"{location}",                        
            "error": f'{error}',
            "token": f'{message}'
        }),
    }

    print(response)
    return response

    


def valdiate_token(event):
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
                return "valid"
            except Exception as e:
                print(f' failed to decoded token {str(e)}')
                return str(e)
    else:
        print('no headers')
        return "no headers to validate"
    
    
    return "n/a"
        
