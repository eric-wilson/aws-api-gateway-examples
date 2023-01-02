import json
import requests
import logging

log = logging.getLogger("users/seed")
location = "users/seed"
def lambda_handler(event, context):
    
    log.info(f'{location}: {json.dumps(event, default=str)}')

    ip = get_ip_address(event=event)
    
    success = seed_users()

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"{location}",
            "location": ip.text.replace("\n", ""),
            "action": f'{success}'
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

def seed_users():
    log.info(f'todo: {location}')

    return False