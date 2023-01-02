import boto3
import logging
from password_algo import generate_hashed_password

location = "common/users"
log = logging.getLogger(f"{location}")
table_name = "ApplicationTable"
dynamodb_client = boto3.client('dynamodb')
dynamodb_resource = boto3.resource('dynamodb')
table = dynamodb_resource.Table(table_name)

log.setLevel('INFO')

def validate_user_login(username, password, application):
    hashed = generate_hashed_password(username, password, application)
    user = get_user(username, application)

    if user is not None:
        pwd_dynamo_obj = user["password"]
        if "S" in pwd_dynamo_obj:
            stored_hashed_pwd = pwd_dynamo_obj["S"]
        else:
            stored_hashed_pwd = pwd_dynamo_obj
        log.info(f'generated hash: {hashed}. db password {stored_hashed_pwd}'
            f' user: {username}'
            f' password raw: {password}'
            f' application: {application}'
        )
    
    if stored_hashed_pwd is not None and hashed == stored_hashed_pwd:
        return True
    
    return False

def get_user(username, application="application_one", include_attributes = False):
    
    
    if include_attributes: 
        response = dynamodb_client.get_item(
            TableName=table_name,
                Key={
                    'pk': {'S': f'user#{username}'},
                    'sk': {'S': f'app#{application}'}
                }
            )
    else:
        
        response = table.get_item(            
                Key={
                    'pk': f'user#{username}',
                    'sk': f'app#{application}'
                }
            )

    log.info(f'user response: {response}')

    try:
        if "Item" in response:
            item = response['Item']
            log.info(f'user item info: {item}')
            return item
        else:
            log.info(f'user not found for {username} / {application}')
            return None
    except Exception as e:
        log.error(f'error getting user: {username} / {application}. {str(e)}')
        return None


def seed_users(event):
    log.info(f'todo: {location}')
    if "users" in event:
        users = event["users"]
        for user in users:
            seed_user(
                user["username"],
                user["password"],
                user["application"],
                user["first_name"],
                user["last_name"],
            )
    
    return False

def seed_user(username, password, application, first_name, last_name):

    hashed_password = generate_hashed_password(username, password, application)

    dynamodb_client.put_item(
        TableName=f'{table_name}', 
        Item={
            'pk':{'S':f'user#{username}'},
            'sk':{'S':f'app#{application}'},
            'password':{'S':f'{hashed_password}'},
            'first_name':{'S':f'{first_name}'},
            'last_name':{'S':f'{last_name}'},
            }
        )