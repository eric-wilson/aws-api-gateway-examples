import json
import logging
import os

try:    
    from common.jwt_token_service import TokenService    
except:
        
    from jwt_token_service import TokenService

location = "/authentication/token/view"
log = logging.getLogger(location)
loglevel = os.getenv("LOG_LEVEL")
# default to info (normal default is warning)
log.setLevel('INFO')

if loglevel:
    log.setLevel(loglevel)


def lambda_handler(event, context):
    
    error = None
    token = None
    try:
        token = get_token(event)
    
    except Exception as e:
        error = str(e)


    return {
        "statusCode": 200,
        "body": json.dumps({
            "location": f"{location}",                        
            "error": f'{error}',
            "token": f'{token}'
        }),
    }

    


def get_token(event):
    if "headers" in event:
        #print('found headers')
        if "authorization" in event["headers"]:
            #print('found authorization')
            encoded = event["headers"]["authorization"]
            ts = TokenService()
            try:
                encoded = str(encoded).removeprefix("Bearer").strip()
                decoded = ts.decode_jwt_token(encoded)
                print(f'decoded: {decoded}')
                return decoded
            except Exception as e:
                message = f' failed to decoded token {str(e)}'
                print(message)
                raise Exception(message)
    else:
        message = 'no headers'
        print(message)
        raise Exception(message)
    
    return None
        
