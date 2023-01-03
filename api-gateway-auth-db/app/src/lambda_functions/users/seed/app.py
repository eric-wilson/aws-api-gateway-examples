import json
import logging

try:
    from common.user_db_actions import seed_users
except:
    from user_db_actions import seed_users

location = "users/seed"
log = logging.getLogger(location)


def lambda_handler(event, context):
    
    log.debug(f'{location}: {json.dumps(event, default=str)}')        
    success = seed_users(event)
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"{location}",            
            "action": f'{success}'
        }),
    }
