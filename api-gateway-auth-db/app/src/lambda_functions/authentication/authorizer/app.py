import json
import logging
import os

try:    
    from users.common.jwt_token_service import TokenService    
except:
        
    from jwt_token_service import TokenService

location = "/authentication/authorizer"
log = logging.getLogger(location)
loglevel = os.getenv("LOG_LEVEL")
SCOPES = os.getenv("ALLOWED_SCOPES")
LOADED_SCOPES = None
# default to info (normal default is warning)
log.setLevel('INFO')

if loglevel:
    log.setLevel(loglevel)


def lambda_handler(event, context):
           
    is_authorized = is_token_authorized(event)
    
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


def is_token_authorized(event):

    is_authorized = False

    if "headers" in event:
        #print('found headers')
        if "authorization" in event["headers"]:
            #print('found authorization')
            encoded = event["headers"]["authorization"]
            ts = TokenService()
            try:
                encoded = str(encoded).removeprefix("Bearer").strip()
                decoded = ts.verify_jwt_token(encoded)
                log.info(f'decoded: {decoded}')
                                
                try:
                    is_authorized = validate_scopes(decoded)
                except Exception as e:
                    log.exception(f'error validating scopes: {str(e)}')
                return is_authorized
            except Exception as e:
                log.exception(f' failed to decoded token {str(e)}')
    else:
        log.info('no headers')
    
    
    return False
        

def validate_scopes(decoded_token):
    log.debug(f'decoded type is {type(decoded_token)}')

    token_scopes = None
    if "scope" in decoded_token:
        scopes = decoded_token["scope"]
        log.debug(f'scope type is: {type(scopes)}')
        log.debug(f'scopes: {scopes}')
        token_scopes = parse_scopes(scopes)


    allowed_scopes = get_allowed_scopes()

    log.debug(f'allowed scopes: {allowed_scopes}')
    log.debug(f'token scopes: {token_scopes}')


    if allowed_scopes is not None:
        for allowed in allowed_scopes:
            if allowed in token_scopes:
                log.debug(f'allowed: {allowed}. exiting')
                return True
            elif allowed == "any":
                log.debug(f'allowed: {allowed}. exiting')
                return True
    else:
        # no scopes are tagged to this so, we'll assume it's ok??
        log.debug(f'no scopes found {allowed_scopes}')
        return False

    # no match is found
    log.debug(f'no scopes matches token with allowed {allowed_scopes}')
    return False
    

def get_allowed_scopes():
    global LOADED_SCOPES
    global SCOPES

    if  LOADED_SCOPES is not None:
        log.info(f'scopes already loaded: {SCOPES}')
        return LOADED_SCOPES
    if SCOPES is not None:
        if type(SCOPES) is str:
            LOADED_SCOPES = parse_scopes(SCOPES)


def parse_scopes(scopes):

    if scopes is not None and type(scopes) is str:
        scopes = scopes.replace("[", "").replace("]", "").replace("'", "").strip()
        scopes = scopes.split(",")
            
        # strip the spaces
        scopes = [x.strip().lower() for x in scopes]

    return scopes